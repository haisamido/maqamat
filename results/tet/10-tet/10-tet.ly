\version "2.24.0"

\header {
  title = "10-tet"
  subtitle = "scale type =10-tet, provided type=by tet, intervals=10, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      cis,1^\markup { "120.0¢" }
      d,1^\markup { "240.0¢" }
      e,1^\markup { "360.0¢" }
      f,1^\markup { "480.0¢" }
      fis,1^\markup { "600.0¢" }
      g,1^\markup { "720.0¢" }
      gis,1^\markup { "840.0¢" }
      ais,1^\markup { "960.0¢" }
      b,1^\markup { "1080.0¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
