SigGraph <- R6::R6Class(
  "SigGraph",
  public = list(
    sig_dat = NULL,
    edges = NULL,
    nodes = NULL,
    graph = NULL,
    aggregation = c("none", "node_context"),
    initialize = function(sig_dat = NULL, source = "template") {
      self$sig_dat <- sig_dat
      self$edges <- self$sig_dat$get_edges()
      self$nodes <- self$sig_dat$get_nodes()
      self$graph <- private$build_graph()
      invisible(self)
    },
    get_graph = function() self$graph,
    refresh = function() {
      # Rebuild the graph based on updated edges and nodes
      self$graph <- private$build_graph()
      invisible(self)
    },
    node_count = function() {
      tidygraph::activate(self$graph, nodes) |>
        dplyr::tally() |>
        dplyr::pull(n)
    },
    edge_count = function() {
      tidygraph::activate(self$graph, edges) |>
        dplyr::tally() |>
        dplyr::pull(n)
    },
    set_aggregation = function(aggregation = c("none", "node_context")) {
      if (aggregation == "node_context") {
        get_node_context <- function(node) {
          if (node %in% self$nodes$node_context) {
            return(node)
          } else {
            node_context <- self$nodes$node_context[self$nodes$node == node]
            if (length(node_context) == 0) {
              warning(paste("Node context not found for node:", node))
              return(NA) # Return NA if not found
            }
            return(node_context)
          }
        }

        # Update edges with new from/to values
        self$edges <- self$edges %>%
          dplyr::mutate(
            from = purrr::map_chr(from, get_node_context),
            to = purrr::map_chr(to, get_node_context)
          )

        context_nodes <- self$nodes %>%
          dplyr::select(node = node_context) %>%
          dplyr::distinct() %>%
          dplyr::mutate(node_context = node)

        self$nodes <- context_nodes

        # Check for NA values after mapping
        if (any(is.na(self$edges$from))) {
          warning("Some 'from' nodes could not be found in the nodes data frame.")
        }
        if (any(is.na(self$edges$to))) {
          warning("Some 'to' nodes could not be found in the nodes data frame.")
        }

        # Refresh the graph only when needed
        self$refresh() # Uncomment this line if you want to refresh automatically
      }
    }
  ),
  private = list(
    build_graph = function() {
      if (!requireNamespace("tidygraph", quietly = TRUE)) {
        stop("Install tidygraph")
      }
      tidygraph::as_tbl_graph(self$edges) |>
        tidygraph::activate(nodes) |>
        dplyr::left_join(self$nodes, by = c("name" = "node")) |>
        dplyr::mutate(
          object = dplyr::if_else(node_context == "humans", node_context, "not human")
        )
    }
  )
)

# Example usage:
# sig_dat <- SigDat$new(source = "template")
# sig_graph <- SigGraph$new(sig_dat = sig_dat)
# g <- sig_graph$get_graph()
