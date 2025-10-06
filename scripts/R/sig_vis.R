SigVis <- R6::R6Class(
  "SigVis",
  public = list(
    sig_graph = NULL,
    graph = NULL,
    initialize = function(source = "template", sig_graph = NULL) {
      self$graph <- sig_graph$graph
    },
    get_graph = function() {
      self$graph
    },
    plot = function() {
      self$graph %>%
        ggraph::ggraph() +
        geom_edge_fan(
          aes(linetype = arrowkeeper, color = status),
          alpha = 0.8
        ) +
        geom_node_point(aes(shape = object),
          size = 20, alpha = 0.1
        ) +
        geom_node_text(aes(label = name)) +
        theme_minimal(
          base_size = 15
        ) +
        theme(
          panel.grid = element_blank(),
          axis.ticks = element_blank(),
          axis.text = element_blank()
        ) +
        labs(
          x = "",
          y = "",
          title = "Structured intelligence governance",
          subtitle = "All elements"
        )
    }
  ),
  private = list()
)
