\version "2.24.0"

\header {
  title = "indian-ratios"
  subtitle = "scale type =indian-ratios, provided type=by ratios, intervals=22, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      cis,1^\markup { "90.2¢" }
      cis,1^\markup { "111.7¢" }
      d,1^\markup { "182.4¢" }
      d,1^\markup { "203.9¢" }
      dis,1^\markup { "294.1¢" }
      dis,1^\markup { "315.6¢" }
      e,1^\markup { "386.3¢" }
      e,1^\markup { "407.8¢" }
      f,1^\markup { "498.0¢" }
      f,1^\markup { "519.6¢" }
      fis,1^\markup { "590.2¢" }
      fis,1^\markup { "611.7¢" }
      g,1^\markup { "702.0¢" }
      gis,1^\markup { "792.2¢" }
      gis,1^\markup { "813.7¢" }
      a,1^\markup { "884.4¢" }
      a,1^\markup { "905.9¢" }
      ais,1^\markup { "996.1¢" }
      ais,1^\markup { "1017.6¢" }
      b,1^\markup { "1088.3¢" }
      b,1^\markup { "1109.8¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
