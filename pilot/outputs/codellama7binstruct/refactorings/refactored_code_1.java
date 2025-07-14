static Result encodeMinimally(Input input) {
        int inputLength = input.length();
        Edge[][] edges = new Edge[inputLength + 1][6];
        addEdges(input, edges, 0, null);
        for (int i = 1; i <= inputLength; i++) {
            for (int j = 0; j < 6; j++) {
                if (edges[i][j] != null && i < inputLength) {
                    addEdges(input, edges, i, edges[i][j]);
                }
            }
            //optimize memory by removing edges that have been passed.
            for (int j = 0; j < 6; j++) {
                edges[i - 1][j] = null;
            }
        }
        int minimalJ = -1;
        int minimalSize = Integer.MAX_VALUE;
        for (int j = 0; j < 6; j++) {
            if (edges[inputLength][j] != null) {
                Edge edge = edges[inputLength][j];
                //C40, TEXT and X12 need an
                int size = j >= 1 && j <= 3 ? edge.cachedTotalSize + 1 : edge.cachedTotalSize;
                // extra unlatch at the end
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