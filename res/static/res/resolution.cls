\LoadClass{article}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resolution}[07/05/2016 EYP Resolution Template]

\RequirePackage{fontspec}
\RequirePackage{titlesec}
\RequirePackage{parskip}
\RequirePackage{enumerate}
\RequirePackage{enumitem}
\RequirePackage{hyperref}
\RequirePackage[a4paper, total={6in, 8in}]{geometry}
\RequirePackage[document]{ragged2e}


\setmainfont{Source Sans Pro}


\titleformat{\section}
  {\huge\scshape\center}
  {}{0em}
  {}


\newcommand{\motion}[1]{
  \begin{large}  
    \textbf{#1}
  \end{large}
}

\newcommand{\submittedby}[1]{
  \begin{tabular}{l p{12cm}}
    Submitted by: & #1
  \end{tabular}
}

\newcommand{\subtopic}[1]{
  \begin{large}
    #1
  \end{large}
}

\newlist{IC}{enumerate}{1}
\setlist[IC]{label=\Alph*.}

\newlist{ICS}{enumerate}{1}
\setlist[ICS]{label=\roman*.}

\newlist{OCS}{enumerate}{1}
\setlist[OCS]{label=\alph*.}
