\version "2.24.0"

\header {
  title = "9-tet"
  subtitle = "scale type =9-tet, provided type=by tet, intervals=9, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      cis,1^\markup { "133.3¢" }
      dis,1^\markup { "266.7¢" }
      e,1^\markup { "400.0¢" }
      f,1^\markup { "533.3¢" }
      g,1^\markup { "666.7¢" }
      gis,1^\markup { "800.0¢" }
      a,1^\markup { "933.3¢" }
      b,1^\markup { "1066.7¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
