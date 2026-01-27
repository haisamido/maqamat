\version "2.24.0"

\header {
  title = "pythagorean-ratios"
  subtitle = "scale type =pythagorean-ratios, provided type=by ratios, intervals=13, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      cis,1^\markup { "90.2¢" }
      d,1^\markup { "203.9¢" }
      dis,1^\markup { "294.1¢" }
      e,1^\markup { "407.8¢" }
      f,1^\markup { "498.0¢" }
      fis,1^\markup { "588.3¢" }
      fis,1^\markup { "611.7¢" }
      g,1^\markup { "702.0¢" }
      gis,1^\markup { "792.2¢" }
      a,1^\markup { "905.9¢" }
      ais,1^\markup { "996.1¢" }
      b,1^\markup { "1109.8¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
