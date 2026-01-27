\version "2.24.0"

\header {
  title = "22-tet"
  subtitle = "scale type =22-tet, provided type=by tet, intervals=22, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      cis,1^\markup { "54.5¢" }
      cis,1^\markup { "109.1¢" }
      d,1^\markup { "163.6¢" }
      d,1^\markup { "218.2¢" }
      dis,1^\markup { "272.7¢" }
      dis,1^\markup { "327.3¢" }
      e,1^\markup { "381.8¢" }
      e,1^\markup { "436.4¢" }
      f,1^\markup { "490.9¢" }
      f,1^\markup { "545.5¢" }
      fis,1^\markup { "600.0¢" }
      g,1^\markup { "654.5¢" }
      g,1^\markup { "709.1¢" }
      gis,1^\markup { "763.6¢" }
      gis,1^\markup { "818.2¢" }
      a,1^\markup { "872.7¢" }
      a,1^\markup { "927.3¢" }
      ais,1^\markup { "981.8¢" }
      ais,1^\markup { "1036.4¢" }
      b,1^\markup { "1090.9¢" }
      b,1^\markup { "1145.5¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
