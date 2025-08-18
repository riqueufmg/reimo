static Result encodeMinimally(Input input) {
    int inputLength = input.length();
    Edge[][] edges = new Edge[inputLength + 1][6];
    addEdges(input, edges, 0, null);
    for (int i = 1; i <= inputLength; i++) {
        addEdges(input, edges, i, edges[i - 1][0]);
        for (int j = 1; j < 6; j++) {
            if (edges[i][j] != null) {
                addEdges(input, edges, i, edges[i][j]);
            }
        }
    }
    int minimalJ = -1;
    int minimalSize = Integer.MAX_VALUE;
    for (int j = 0; j < 6; j++) {
        if (edges[inputLength][j] != null) {
            Edge edge = edges[inputLength][j];
            int size = j >= 1 && j <= 3 ? edge.cachedTotalSize + 1 : edge.cachedTotalSize;
            if (size < minimalSize) {
                minimalSize = size;
                minimalJ = j;
            }
        }
    }
    if (minimalJ < 0) {
        throw new IllegalStateException("Failed to encode \"" + input + "\"");
    }
    return new Result(edges[inputLength][minimalJ]);
}
