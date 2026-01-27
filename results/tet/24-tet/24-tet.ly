\version "2.24.0"

\header {
  title = "24-tet"
  subtitle = "scale type =24-tet, provided type=by tet, intervals=24, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      c,1^\markup { "50.0¢" }
      cis,1^\markup { "100.0¢" }
      d,1^\markup { "150.0¢" }
      d,1^\markup { "200.0¢" }
      d,1^\markup { "250.0¢" }
      dis,1^\markup { "300.0¢" }
      e,1^\markup { "350.0¢" }
      e,1^\markup { "400.0¢" }
      e,1^\markup { "450.0¢" }
      f,1^\markup { "500.0¢" }
      fis,1^\markup { "550.0¢" }
      fis,1^\markup { "600.0¢" }
      fis,1^\markup { "650.0¢" }
      g,1^\markup { "700.0¢" }
      gis,1^\markup { "750.0¢" }
      gis,1^\markup { "800.0¢" }
      gis,1^\markup { "850.0¢" }
      a,1^\markup { "900.0¢" }
      ais,1^\markup { "950.0¢" }
      ais,1^\markup { "1000.0¢" }
      ais,1^\markup { "1050.0¢" }
      b,1^\markup { "1100.0¢" }
      c1^\markup { "1150.0¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
