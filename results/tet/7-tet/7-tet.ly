\version "2.24.0"

\header {
  title = "7-tet"
  subtitle = "scale type =7-tet, provided type=by tet, intervals=7, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      d,1^\markup { "171.4¢" }
      dis,1^\markup { "342.9¢" }
      f,1^\markup { "514.3¢" }
      g,1^\markup { "685.7¢" }
      a,1^\markup { "857.1¢" }
      ais,1^\markup { "1028.6¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
