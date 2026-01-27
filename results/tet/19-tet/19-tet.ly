\version "2.24.0"

\header {
  title = "19-tet"
  subtitle = "scale type =19-tet, provided type=by tet, intervals=19, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      cis,1^\markup { "63.2¢" }
      cis,1^\markup { "126.3¢" }
      d,1^\markup { "189.5¢" }
      dis,1^\markup { "252.6¢" }
      dis,1^\markup { "315.8¢" }
      e,1^\markup { "378.9¢" }
      e,1^\markup { "442.1¢" }
      f,1^\markup { "505.3¢" }
      fis,1^\markup { "568.4¢" }
      fis,1^\markup { "631.6¢" }
      g,1^\markup { "694.7¢" }
      gis,1^\markup { "757.9¢" }
      gis,1^\markup { "821.1¢" }
      a,1^\markup { "884.2¢" }
      a,1^\markup { "947.4¢" }
      ais,1^\markup { "1010.5¢" }
      b,1^\markup { "1073.7¢" }
      b,1^\markup { "1136.8¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
