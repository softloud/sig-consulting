# Simple SIG data loader (public Google Sheet, no auth needed)

SigDat <- R6::R6Class(
  "SigDat",
  public = list(
    edges = NULL,
    nodes = NULL,
    sheet_id = NULL,
    source = NULL,
    initialize = function(source = c("template", "client"), env_template = "client_credentials/.env",
                          env_client = "client_credentials/.env-client") {
      self$source <- match.arg(source)
      env_file <- if (self$source == "template") env_template else env_client

      if (file.exists(env_file)) {
        if (!requireNamespace("dotenv", quietly = TRUE)) stop("Install 'dotenv'")
        dotenv::load_dot_env(env_file)
      }

      # Public sheet: no auth
      if (!requireNamespace("googlesheets4", quietly = TRUE)) stop("Install 'googlesheets4'")
      googlesheets4::gs4_deauth()

      self$sheet_id <- Sys.getenv("GS_SHEET_ID", unset = NA)
      if (is.na(self$sheet_id) || self$sheet_id == "") {
        url <- Sys.getenv("GS_DATA_ENTRY_URL", unset = "")
        m <- regmatches(url, regexpr("(?<=/d/)[A-Za-z0-9-_]+", url, perl = TRUE))
        if (length(m)) self$sheet_id <- m
      }
      if (is.na(self$sheet_id) || self$sheet_id == "") stop("Sheet ID not found in env vars.")

      self$edges <- self$read_sheet_simple("edges")
      self$nodes <- self$read_sheet_simple("nodes")
    },
    read_sheet_simple = function(sheet_name) {
      googlesheets4::read_sheet(ss = self$sheet_id, sheet = sheet_name, .name_repair = "minimal")
    },
    refresh = function() {
      self$edges <- self$read_sheet_simple("edges")
      self$nodes <- self$read_sheet_simple("nodes")
      invisible(self)
    },
    get_edges = function() self$edges,
    get_nodes = function() self$nodes
  )
)

# Example usage:
# sig_dat <- SigDat$new(source = "client")
# sig_dat$get_edges()
# sig_dat$get_nodes()
