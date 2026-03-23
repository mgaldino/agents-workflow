# ============================================================================
# Download OECD Tariff Data from World Bank WDI using R
# ============================================================================
#
# This R script downloads weighted-mean and simple-mean tariff rates
# for all OECD member countries (as of 2010) for the period 2000-2010.
#
# Data source: World Bank World Development Indicators (WDI)
#
# Usage:
#   install.packages(c("WDI", "tidyverse"))
#   source("download_tariffs.R")
#
# Output:
#   oecd_tariffs_wdi_2000_2010.csv
# ============================================================================

library(WDI)
library(dplyr)
library(tidyr)

# --- OECD member countries as of 2010 (ISO2 codes) ---
oecd_iso2 <- c(
  "AU", "AT", "BE", "CA", "CL", "CZ", "DK", "FI", "FR", "DE",
  "GR", "HU", "IS", "IE", "IT", "JP", "KR", "LU", "MX", "NL",
  "NZ", "NO", "PL", "PT", "SK", "ES", "SE", "CH", "TR", "GB", "US"
)

# --- WDI Tariff indicators ---
indicators <- c(
  "TM.TAX.MRCH.WM.AR.ZS",  # Tariff rate, applied, weighted mean, all products (%)
  "TM.TAX.MRCH.SM.AR.ZS",  # Tariff rate, applied, simple mean, all products (%)
  "TM.TAX.MRCH.WM.FN.ZS",  # Tariff rate, applied, weighted mean, manufactured products (%)
  "TM.TAX.TCOM.WM.AR.ZS"   # Tariff rate, applied, weighted mean, primary products (%)
)

# --- Download data ---
cat("Downloading tariff data from World Bank WDI...\n")

tariff_data <- WDI(
  country = oecd_iso2,
  indicator = indicators,
  start = 2000,
  end = 2010,
  extra = TRUE  # includes income group, region, etc.
)

# --- Rename columns for clarity ---
tariff_data <- tariff_data %>%
  rename(
    tariff_weighted_mean_all = TM.TAX.MRCH.WM.AR.ZS,
    tariff_simple_mean_all = TM.TAX.MRCH.SM.AR.ZS,
    tariff_weighted_mean_manuf = TM.TAX.MRCH.WM.FN.ZS,
    tariff_weighted_mean_primary = TM.TAX.TCOM.WM.AR.ZS
  )

# --- Sort ---
tariff_data <- tariff_data %>%
  arrange(iso3c, year)

# --- Save ---
output_path <- file.path(dirname(sys.frame(1)$ofile), "oecd_tariffs_wdi_2000_2010.csv")
write.csv(tariff_data, output_path, row.names = FALSE)
cat(sprintf("Saved %d rows to %s\n", nrow(tariff_data), output_path))

# --- Summary statistics ---
cat("\n--- Summary ---\n")
cat(sprintf("Countries: %d\n", n_distinct(tariff_data$iso3c)))
cat(sprintf("Years: %d to %d\n", min(tariff_data$year), max(tariff_data$year)))
cat(sprintf("Total observations: %d\n", nrow(tariff_data)))

cat("\nMissing values:\n")
tariff_data %>%
  summarise(
    across(
      starts_with("tariff_"),
      ~ sum(is.na(.)),
      .names = "{.col}"
    )
  ) %>%
  pivot_longer(everything(), names_to = "indicator", values_to = "n_missing") %>%
  mutate(pct_missing = round(100 * n_missing / nrow(tariff_data), 1)) %>%
  print()

cat("\nMean tariff by year (weighted mean, all products):\n")
tariff_data %>%
  group_by(year) %>%
  summarise(
    mean_tariff = mean(tariff_weighted_mean_all, na.rm = TRUE),
    median_tariff = median(tariff_weighted_mean_all, na.rm = TRUE),
    n_countries = sum(!is.na(tariff_weighted_mean_all))
  ) %>%
  print(n = Inf)


# ============================================================================
# Alternative: Download from WITS using tradestatistics package
# ============================================================================
#
# If you need product-level tariffs:
#
# install.packages("tradestatistics")
# library(tradestatistics)
#
# # Get tariff data for a specific country and year
# us_tariffs <- ots_create_tidy_data(
#   years = 2000:2010,
#   reporters = "usa",
#   table = "yr"
# )
#
# # Note: tradestatistics focuses on trade flows, not tariffs.
# # For product-level tariffs, use the WITS web interface or the
# # world_trade_data Python package.
# ============================================================================
