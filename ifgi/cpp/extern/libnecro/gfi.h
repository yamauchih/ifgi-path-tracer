/*
 * Copyright (c) 2011 Matthias Raab <iovis@gmx.net>
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

/* 
   Read and write lightgrinder floating point images.
   (simple, uncompressed, 32 bit floating point precision, high dynamic range
   image file format)

   Pixels are stored as single array of tuples, e.g. (rgbrgb...) for a 
   3-channel RGB image, scanlines ordered from top to bottom (if an
   application has a different scanline order: both reading and writing
   support reversing the scanline order).

   This header is self-contained and should work with every C99 compiler, the 
   only noteworthy thing is that big endian platform have to define
   GFI_BIG_ENDIAN to create portable files.
*/

#ifndef GRIND_FLOAT_IMAGE_H_
#define GRIND_FLOAT_IMAGE_H_

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#define GFI_VERSION 1
#define GFI_APP_NAME_LEN 32

/* minimal header version 1, guaranteed to be compatible with future versions */
typedef struct {
     /* gfi version */
     uint32_t version;
     /* image size */
     uint32_t res_x, res_y;
     /* color channels in image */
     uint32_t num_channels;
     /* application name this image was created with */
     char application_name[GFI_APP_NAME_LEN];
     /* gamma which has been applied, usually 1.0 */
     float gamma;
     /* offset to pixel data, internal, don't change */
     uint32_t offset;
} gfi_image_header;

/* initialize header with application name */
static inline void gfi_init_image_header(
     gfi_image_header * const header, const char *application_name)
{
     memset(header, 0, sizeof(gfi_image_header));
     header->version = GFI_VERSION;
     strncpy(header->application_name, application_name, GFI_APP_NAME_LEN - 1);
     header->gamma = 1.0f;
}

/* error codes than can be reported */
typedef enum {
     GFI_SUCCESS = 0,
     GFI_ERROR_INVALID_HEADER = 1,
     GFI_ERROR_READING_HEADER = 2,
     GFI_ERROR_READING_PIXELS = 3,
     GFI_ERROR_ALLOCATION_FAILURE = 4,
     GFI_ERROR_WRITING_HEADER = 5,
     GFI_ERROR_WRITING_PIXELS = 6,
     GFI_ERROR_NUM_CODES = 7
} gfi_error_code;

/* strings for each error code */
static const char * const gfi_error_codes[GFI_ERROR_NUM_CODES] =
{
     "no error",
     "invalid header",
     "error reading header from file",
     "error reading pixels from file",
     "cannot allocate memory for pixels",
     "error writing header to file",
     "error writing pixels to file"
};

/* get string for an error code */
static inline const char *gfi_get_error_str(const gfi_error_code code)
{
     if (code >= GFI_ERROR_NUM_CODES)
	  return 0;
     else
	  return gfi_error_codes[code];
}

/* default storage is little endian, on big endian platforms bytes need to be swapped */
#ifdef GFI_BIG_ENDIAN
static inline void GFI_SWAP_32(unsigned int * const i) {
     *i = ((*i << 24) | ((*i << 8) & 0x00ff0000) | ((*i >> 8) & 0x0000ff00) | (*i >>24));
}
static inline void GFI_SWAP_HEADER(gfi_image_header * const header) {
     GFI_SWAP32(&header->version);
     GFI_SWAP32(&header->res_x);
     GFI_SWAP32(&header->res_y);
     GFI_SWAP32(&header->num_channels);
     GFI_SWAP32(&header->offset);
     GFI_SWAP32(&header->gamma);     
}
static inline void GFI_SWAP_PIXELS(const void * const f, const uint32_t n) {
     unsigned int * const p = (unsigned int * const)f;
     for (uint32_t i = 0; i < n; ++i)
	  GFI_SWAP32(p + i);
}
#else
#define GFI_SWAP_HEADER(p) {}
#define GFI_SWAP_PIXELS(p, s) {}
#endif

static const unsigned int gfi_header_str_len = 16;
static const char gfi_header_str[17] = "GRIND_FLOAT_IMG_";

static inline gfi_error_code gfi_check_header_data(
     const gfi_image_header * const header)
{
     if (header->res_x == 0 || 
	 header->res_y == 0 ||
	 header->num_channels == 0)
	  return GFI_ERROR_INVALID_HEADER;
     else 
	  return GFI_SUCCESS;
}

/* read header of a .gfi image file */
static inline gfi_error_code gfi_read_image_header(
     gfi_image_header * const header, FILE * const fp)
{
     rewind(fp);
     char buf[gfi_header_str_len];
     size_t size = fread(buf, 1, gfi_header_str_len, fp);
     if (size != gfi_header_str_len)
	  return GFI_ERROR_READING_HEADER;
     if (strncmp(buf, gfi_header_str, gfi_header_str_len) != 0)
	  return GFI_ERROR_INVALID_HEADER;
     
     size = fread(header, sizeof(gfi_image_header), 1, fp);
     if (size != 1)
	  return GFI_ERROR_READING_HEADER;
     
     GFI_SWAP_HEADER(header);

     return gfi_check_header_data(header);
}

/* read pixels of a .gfi image file into (preallocated) array */
static inline gfi_error_code gfi_read_image_pixels(
     const gfi_image_header * const header,
     float * const pixels,
     const int reverse_scanlines,
     FILE * const fp)
{
     const int i = fseek(fp, header->offset, SEEK_SET);
     if (i == -1)
	  return GFI_ERROR_READING_PIXELS;
    
     const uint32_t n = header->num_channels * header->res_x;
     for (uint32_t j = 0; j < header->res_y; ++j)
     {
	  const uint32_t idx = reverse_scanlines ? (header->res_y - j - 1) * n : j * n;
	  if (fread(pixels + idx, sizeof(float), n, fp) != n)
	       return GFI_ERROR_READING_PIXELS;
	  GFI_SWAP_PIXELS(pixels + idx, n);
     }

     return GFI_SUCCESS;
}

/* read header & pixels of a .gfi image file, pixels are allocated using malloc */
static inline gfi_error_code gfi_read_image(
     gfi_image_header * const header,
     float ** const pixels,
     const int reverse_scanlines,
     FILE * const fp)
{
     gfi_error_code code;
     if ((code = gfi_read_image_header(header, fp)) != GFI_SUCCESS)
	  return code;
     
     const uint32_t n = header->num_channels * header->res_x * header->res_y;
     *pixels = (float *)malloc(n * sizeof(float));
     if (!(*pixels))
	  return GFI_ERROR_ALLOCATION_FAILURE;

     return gfi_read_image_pixels(header, *pixels, reverse_scanlines, fp);
}

/* write header for a .gfi image file */
static inline gfi_error_code gfi_write_image_header(
     gfi_image_header * const header,
     FILE * const fp)
{
     rewind(fp);
     size_t size = fwrite(gfi_header_str, sizeof(char), gfi_header_str_len, fp);
     if (size != gfi_header_str_len)
	  return GFI_ERROR_WRITING_HEADER;
         
     const gfi_error_code code = gfi_check_header_data(header);
     if (code != GFI_SUCCESS)
	  return code;

     header->offset = gfi_header_str_len + sizeof(gfi_image_header);
     
     GFI_SWAP_HEADER(header);
     size = fwrite(header, sizeof(gfi_image_header), 1, fp);
     GFI_SWAP_HEADER(header);
     if (size != 1)
	  return GFI_ERROR_WRITING_HEADER;

     return GFI_SUCCESS;
}

/* write pixels to a .gfi image file, the header has to been written already */
static inline gfi_error_code gfi_write_image_pixels(
     const gfi_image_header * const header,
     float * const pixels,
     const int reverse_scanlines,
     FILE * const fp)
{
     const int i = fseek(fp, header->offset, SEEK_SET);
     if (i == -1)
	  return GFI_ERROR_WRITING_PIXELS;
  
     const uint32_t n = header->num_channels * header->res_x;
     for (uint32_t j = 0; j < header->res_y; ++j)
     {
	  const uint32_t idx = reverse_scanlines ? (header->res_y - j - 1) * n : j * n;
	  GFI_SWAP_PIXELS(pixels + idx, n);
	  const size_t size = fwrite(pixels + idx, sizeof(float), n, fp);
	  GFI_SWAP_PIXELS(pixels + idx, n);
	  if (size != n)
	       return GFI_ERROR_WRITING_PIXELS;
     }
     return GFI_SUCCESS;
}

/* write header & pixels of a .gfi image file */
static inline gfi_error_code gfi_write_image(
     gfi_image_header * const header,
     float * const pixels,
     const int reverse_scanlines,
     FILE * const fp)
{
     const gfi_error_code code = gfi_write_image_header(header, fp);
     if (code != GFI_SUCCESS)
	  return code;
     
     return gfi_write_image_pixels(header, pixels, reverse_scanlines, fp);
}

#endif /* GRIND_FLOAT_IMAGE_H_ */
