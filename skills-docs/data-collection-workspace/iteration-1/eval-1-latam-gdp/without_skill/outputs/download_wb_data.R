# ===========================================================================
# Download GDP per capita and Population for Latin American countries
# from the World Bank (WDI) using the {WDI} R package.
#
# Indicators:
#   NY.GDP.PCAP.CD  -- GDP per capita (current US$)
#   SP.POP.TOTL     -- Population, total
#
# Coverage: 20 Latin American countries, 2000-2023
#
# Usage:
#   install.packages(c("WDI", "tidyverse"))
#   source("download_wb_data.R")
# ===========================================================================

library(WDI)
library(dplyr)
library(tidyr)
library(readr)

# -------------------------------------------------------------------------- #
# 1. Latin American country ISO-2 codes (WDI uses ISO-2 by default)
# -------------------------------------------------------------------------- #
latam_iso2 <- c(
  "AR",  # Argentina
  "BO",  # Bolivia
  "BR",  # Brazil
  "CL",  # Chile
  "CO",  # Colombia
  "CR",  # Costa Rica
  "CU",  # Cuba
  "DO",  # Dominican Republic
  "EC",  # Ecuador
  "SV",  # El Salvador
  "GT",  # Guatemala
  "HT",  # Haiti
  "HN",  # Honduras
  "MX",  # Mexico
  "NI",  # Nicaragua
  "PA",  # Panama
  "PY",  # Paraguay
  "PE",  # Peru
  "UY",  # Uruguay
  "VE"   # Venezuela
)

# -------------------------------------------------------------------------- #
# 2. Download data
# -------------------------------------------------------------------------- #
cat("Downloading GDP per capita and population from World Bank...\n")

panel <- WDI(
  indicator = c(
    gdp_per_capita_current_usd = "NY.GDP.PCAP.CD",
    population                 = "SP.POP.TOTL"
  ),
  country = latam_iso2,
  start   = 2000,
  end     = 2023,
  extra   = TRUE   # includes iso3c, region, income level, etc.
)

# -------------------------------------------------------------------------- #
# 3. Clean and arrange
# -------------------------------------------------------------------------- #
panel <- panel %>%
  select(
    iso2c,
    iso3c,
    country_name = country,
    year,
    gdp_per_capita_current_usd,
    population,
    region,
    income
  ) %>%
  arrange(iso3c, year)

cat(sprintf("Panel dimensions: %d rows x %d columns\n", nrow(panel), ncol(panel)))
cat(sprintf("Countries: %d\n", n_distinct(panel$iso3c)))
cat(sprintf("Years: %d-%d\n", min(panel$year), max(panel$year)))

# -------------------------------------------------------------------------- #
# 4. Save outputs
# -------------------------------------------------------------------------- #
output_dir <- dirname(sys.frame(1)$ofile)  # directory of this script
if (is.null(output_dir)) output_dir <- getwd()

# Long format (panel)
long_path <- file.path(output_dir, "latam_gdp_pcap_population_panel.csv")
write_csv(panel, long_path)
cat(sprintf("Saved: %s\n", long_path))

# Wide format - GDP per capita
gdp_wide <- panel %>%
  select(iso3c, country_name, year, gdp_per_capita_current_usd) %>%
  pivot_wider(
    names_from  = year,
    values_from = gdp_per_capita_current_usd,
    names_prefix = "gdp_pcap_"
  )
write_csv(gdp_wide, file.path(output_dir, "latam_gdp_pcap_wide.csv"))

# Wide format - Population
pop_wide <- panel %>%
  select(iso3c, country_name, year, population) %>%
  pivot_wider(
    names_from  = year,
    values_from = population,
    names_prefix = "pop_"
  )
write_csv(pop_wide, file.path(output_dir, "latam_population_wide.csv"))

cat("Done.\n")
