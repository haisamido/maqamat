\version "2.24.0"

\header {
  title = "5-tet"
  subtitle = "scale type =5-tet, provided type=by tet, intervals=5, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      d,1^\markup { "240.0¢" }
      f,1^\markup { "480.0¢" }
      g,1^\markup { "720.0¢" }
      ais,1^\markup { "960.0¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
