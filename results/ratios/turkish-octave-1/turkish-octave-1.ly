\version "2.24.0"

\header {
  title = "turkish-octave-1"
  subtitle = "scale type =turkish-octave-1, provided type=by ratios, intervals=24, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      cis,1^\markup { "90.2¢" }
      cis,1^\markup { "113.7¢" }
      d,1^\markup { "180.4¢" }
      d,1^\markup { "203.9¢" }
      dis,1^\markup { "294.1¢" }
      dis,1^\markup { "317.6¢" }
      e,1^\markup { "384.4¢" }
      e,1^\markup { "407.8¢" }
      f,1^\markup { "498.0¢" }
      f,1^\markup { "521.5¢" }
      fis,1^\markup { "588.3¢" }
      fis,1^\markup { "611.7¢" }
      g,1^\markup { "678.5¢" }
      g,1^\markup { "702.0¢" }
      gis,1^\markup { "792.2¢" }
      gis,1^\markup { "815.6¢" }
      a,1^\markup { "882.4¢" }
      a,1^\markup { "905.9¢" }
      ais,1^\markup { "996.1¢" }
      ais,1^\markup { "1019.6¢" }
      b,1^\markup { "1086.3¢" }
      b,1^\markup { "1109.8¢" }
      c1^\markup { "1176.5¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
