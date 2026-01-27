\version "2.24.0"

\header {
  title = "just-intonation-ratios"
  subtitle = "scale type =just-intonation-ratios, provided type=by ratios, intervals=13, f0=440Hz"
  tagline = ##f
}

\score {
  \new Staff {
    \clef "bass"
    \cadenzaOn
    \absolute {
      c,1^\markup { "0.0¢" }
      cis,1^\markup { "111.7¢" }
      d,1^\markup { "203.9¢" }
      dis,1^\markup { "315.6¢" }
      e,1^\markup { "386.3¢" }
      f,1^\markup { "498.0¢" }
      fis,1^\markup { "590.2¢" }
      fis,1^\markup { "609.8¢" }
      g,1^\markup { "702.0¢" }
      gis,1^\markup { "813.7¢" }
      a,1^\markup { "884.4¢" }
      ais,1^\markup { "1017.6¢" }
      b,1^\markup { "1088.3¢" }
      c1^\markup { "1200.0¢" }
    }
  }
  \layout { }
}
