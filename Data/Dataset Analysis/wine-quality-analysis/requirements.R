required_packages <- c(
  "tidyverse",
  "readr",
  "fBasics",
  "ggplot2",
  "dplyr",
  "GGally",
  "FactoMineR",
  "factoextra",
  "lmtest",
  "knitr"
)

installed_packages <- rownames(installed.packages())
missing_packages <- required_packages[
  !(required_packages %in% installed_packages)
]

if (length(missing_packages) > 0) {
  install.packages(missing_packages)
}
