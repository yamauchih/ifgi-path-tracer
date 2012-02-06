;;
;; Utility functions of transforming python file to cpp file
;; Copyright (C) 2011-2012 Yamauchi Hitoshi
;;

;; symbol list
(setq python-cpp-symbol-replace-list
      (list
       '("def __str__()" "std::string to_string() const")
       '("self, "  "")                  ; remove 'self, '
       '("self\\." "this->")            ; 'self.' -> 'this->'
       '("self"    "")                  ; remove 'self'
       '("\"\"\""  "/// ")
       '("# "      "/// ")
       '("\'"      "\"")
       '("):"      "){")
       '(")$"      ");")
       '("\\$"      "")                 ; remove trailing backslash
       '(" _"       " ")
       '(" and "    " && ")
       '(" or "     " || ")
       '("numpy.cross" "cross")
       '("numpy.dot"   "dot")
       '("this->__"    "m_")               ; members
       '("math.pi"     "M_PI")
       '("math.sin"    "sin")
       '("math.cos"    "cos")
       '("math.tan"    "tan")
       '("math.sqrt"   "sqrt")
       '("elif"        "else if")
       '("\\(^[ \t]*\\)\\(\\\\return\\)" "\\1/// \\2")
       '("\\(^[ \t]*\\)\\(\\\\param\\)" "\\1/// \\2")

       ;; ;; QFileDialog
       ;; '("QFileDialog(\\(.*\\),[ \t\n]*\\(\".*\"\\),[ \t\n]*\\(.*\\))"
       ;;   "QFileDialog(\\1);\npO->setObjectName(\\2);\npO->setModal(\\3);")
       ;; '("setMode(QFileDialog::\\(.*\\))"
       ;;   "setFileMode(QFileDialog::\\1)")

       ;; ;; sstreamcomp
       ;; '("base/sstreamcomp.hh" "sstream")

       ;; ;;
       ;; '("gmu/Incoming/hitoshi/Geometry/MST" "gmu/Tools/MST")
       ;; '("gmu/Incoming/hitoshi/Common/DP"    "gmu/Common/DataProc")
       ;; '("gmu/Incoming/hitoshi/Common/ModVisMeshScalar.hh"
       ;;   "gmu/Common/VisMeshScalar/ModVisMeshScalar.hh")
       ;; '("gmu/Incoming/hitoshi/Common/VMS"   "gmu/Common/VisMeshScalar")
       ;; '("gmu/Incoming/hitoshi/Common"       "gmu/Common")
       ;; '("GMU::Geometry::Dijkstra"    "GMU::MST::Dijkstra")
       ))

(defun replace-python-to-cpp (b e)
  "Replace python symbols to cpp symbols"
  (interactive "r")
  (save-excursion
    (save-restriction
      (narrow-to-region b e)
      (let
	  ((python-sym-list python-cpp-symbol-replace-list))
	(while python-sym-list
	  (let ((org (car (car python-sym-list)))
		(dst (car (cdr (car python-sym-list)))))
	    (goto-char b)
	    (replace-regexp org dst)
	    (setq python-sym-list (cdr python-sym-list))))))))

(defun query-replace-python-to-cpp (b e)
  "Query replace python symbols to cpp symbols"
  (interactive "r")
  (save-excursion
    (save-restriction
      (narrow-to-region b e)
      (let
	  ((python-sym-list python-cpp-symbol-replace-list))
	(while python-sym-list
	  (let ((org (car (car python-sym-list)))
		(dst (car (cdr (car python-sym-list)))))
	    (goto-char b)
	    (query-replace-regexp org dst)
	    (setq python-sym-list (cdr python-sym-list))))))))


;;
;; insert cpp header
;;
(defun insert-c++-header ()
  "insert c++ header
"
  (interactive)
  (let* (
         (abspath  (buffer-file-name))
         (fname    (file-name-nondirectory abspath))
         (incguard (upcase abspath))
         (ns-name  "ifgi")
        )
    ;; I could not find direct string manipuration, so use a temporary
    ;; buffer. This is powerful, but, I feel a bit overkill.
    ;; make a include guard from absolute pathname.
    (with-temp-buffer
      (progn
        (insert-string incguard)
        ;; special for ifgi. Cut the project path
        (replace-string "/home/hitoshi/data/project/" "" nil (point-min) (point-max))
        ;; in general
        (replace-string "/" "_" nil (point-min) (point-max))
        (replace-string "-" "_" nil (point-min) (point-max))
        (replace-string "." "_" nil (point-min) (point-max))
        (setq incguard (buffer-substring (point-min) (point-max)))
        ))
    (insert-string
     (format
      "//----------------------------------------------------------------------
// ifgi c++ implementation: %s
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \\file
/// \\brief %s
#ifndef %s
#define %s
namespace %s
{
} // namespace %s
#endif // #ifndef %s
" fname fname incguard incguard ns-name ns-name incguard))))



