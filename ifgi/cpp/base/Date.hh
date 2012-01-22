//----------------------------------------------------------------------
// ifgi c++ implementation: Date.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief java.util.Date like Date class. based on base/util/Date.hh
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_DATE_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_DATE_HH

#include <cstdio>
#include <string>
#include <iostream>
#include <sys/time.h>

namespace ifgi
{
/**
   \class Date Date.hh
   \brief get current date, time, and their string representation

   One of this class's usage is to record time. Fro example, the next
   code put a timestamp.
   <code>
base::Date
std::cout << "# generated on " << curTime.toCTimeStr() << std::endl;
   </code>

   The origin of some method names are from java.util.Date.
   \see     test_Date.C
*/
class Date
{
public:
  /**
     constructor
     keep the current date to this object
  */
  Date(){
    struct timezone tz;
    const int r = gettimeofday(&(this->mDateTime), &tz);
    if(r != 0){
      std::cerr << "Error! : base::Date::Date() : can not call gettimeofday."
		<< std::endl;
      this->mDateTime.tv_sec  = 0L;
      this->mDateTime.tv_usec = 0L;
    }
  }

  /**
     construct with specified number of seconds since the standard
     base time known as "the epoch", namely 1970-1-1 00:00:00
     GMT.

     \param sec  the number of seconds
     \param usec the number of microseconds
  */
  Date(long sec, long usec){
    this->setTime(sec, usec);
  }

  /**
     copy constructor
  */
  Date(const Date& aDate){
    this->setTime(aDate.mDateTime.tv_sec, aDate.mDateTime.tv_usec);
  }

  /**
     substitution
  */
  const Date& operator=(const Date& rhs){
    if(this != &rhs){
      this->mDateTime = rhs.mDateTime;
    }
    return(*this);
  }

  /**
     get the number of seconds since 1970-1-1 00:00:00.

     @return get the number of seconds since 1970-1-1 00:00:00 of
     this instance.
  */
  long getTime() const {
    return(this->mDateTime.tv_sec);
  }

  /**
     get the number of microseconds part only, if you want to know the
     second part, use getTime, @see getTime

     @return get the microseconds part
  */
  long getMicrosecTime() const {
    return(this->mDateTime.tv_usec);
  }

  /**
     get time as a double number for easy calculation.

     @return get the current time from the epoch time as a double
     number.
  */
  double getTimeAsDouble() const {
    double t = (double)(this->getTime()) +
      1.0e-6 * (double)(this->getMicrosecTime());
    return(t);
  }

  /**
     set this Date object with seconds after 1970-1-1 00:00:00.

     @param sec  the number of seconds
     @param usec the number of microseconds
  */
  void setTime(long sec, long usec){
    this->mDateTime.tv_sec  = sec;
    this->mDateTime.tv_usec = usec;
  }

  /**
     test if this date is before the specified date.

     @param   aDate a date.
     @return true iff this instance is earlier than aDate (not even
     equal), otherwise false.
  */
  bool before(const Date& aDate) const {
    if(this->getTime() < aDate.getTime()){
      return(true);
    }
    else if(this->getTime() == aDate.getTime()){
      if(this->getMicrosecTime() < aDate.getMicrosecTime()){
	return(true);
      }
    }
    return(false);
  }

  /**
     test if this date is after the specified date.

     @param   aDate a date.
     @return  true iff this instance is later than aDate (not even
     equal), otherwise false.
  */
  bool after(const Date& aDate) const{
    if(this->getTime() > aDate.getTime()){
      return(true);
    }
    else if(this->getTime() == aDate.getTime()){
      if(this->getMicrosecTime() > aDate.getMicrosecTime()){
	return(true);
      }
    }
    return(false);
  }

  /**
     test if two dates are equal.

     @param   aDate the date to compare with.
     @return  true iff the dates are the same, otherwise false.
  */
  bool equals(const Date& aDate) const {
    return((this->getTime()         == aDate.getTime()) &&
	   (this->getMicrosecTime() == aDate.getMicrosecTime()));
  }

  /* *
     get a hash code.
     @return  a hash code value for this object.
  */
  //   int hashCode()
  //   {
  //   }

  /**
     a string representation of this instance

     @return a string representation of this instance
  */
  std::string toString() const{
    const int NBUF = 64;
    char buf[NBUF];
    snprintf(buf, NBUF, "%ld %ld", this->mDateTime.tv_sec, this->mDateTime.tv_usec);
    return(std::string(buf));
  }

  /**
     string representation of this instance using ctime

     @return a string representation of this instance using ctime
  */
  std::string toCTimeStr() const{
    // ctime needs time_t
    std::string tstr(ctime(&(this->mDateTime.tv_sec)));
    // chop the last \n
    std::string::size_type p0 = tstr.size() - 1;
    std::string::size_type p1 = p0 + 1;
    tstr.erase(p0, p1);

    return(tstr);
  }

private:
  ///
  struct timeval mDateTime;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_DATE_HH
