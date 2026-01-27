\version "2.24.0"

\header {
  title = "17-tet"
  subtitle = "scale type =17-tet, provided type=by tet, intervals=17, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      cis,1^\markup { "70.6¢" }
      cis,1^\markup { "141.2¢" }
      d,1^\markup { "211.8¢" }
      dis,1^\markup { "282.4¢" }
      e,1^\markup { "352.9¢" }
      e,1^\markup { "423.5¢" }
      f,1^\markup { "494.1¢" }
      fis,1^\markup { "564.7¢" }
      fis,1^\markup { "635.3¢" }
      g,1^\markup { "705.9¢" }
      gis,1^\markup { "776.5¢" }
      gis,1^\markup { "847.1¢" }
      a,1^\markup { "917.6¢" }
      ais,1^\markup { "988.2¢" }
      b,1^\markup { "1058.8¢" }
      b,1^\markup { "1129.4¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
