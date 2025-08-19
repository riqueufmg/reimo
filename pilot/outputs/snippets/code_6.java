/**
 *     Run a depth-first filtered traversal of the root and all of its descendants.
 *     @param filter NodeFilter visitor.
 *     @param root the root node point to traverse.
 *     @return The filter result of the root node, or {@link FilterResult#STOP}.
 *
 *     @see NodeFilter
 */
public static FilterResult filter(NodeFilter filter, Node root) {
    Node node = root;
    int depth = 0;
    while (node != null) {
        FilterResult result = filter.head(node, depth);
        if (result == FilterResult.STOP)
            return result;
        // Descend into child nodes:
        if (result == FilterResult.CONTINUE && node.childNodeSize() > 0) {
            node = node.childNode(0);
            ++depth;
            continue;
        }
        // No siblings, move upwards:
        while (true) {
            // depth > 0, so has parent
            assert node != null;
            if (!(node.nextSibling() == null && depth > 0))
                break;
            // 'tail' current node:
            if (result == FilterResult.CONTINUE || result == FilterResult.SKIP_CHILDREN) {
                result = filter.tail(node, depth);
                if (result == FilterResult.STOP)
                    return result;
            }
            // In case we need to remove it below.
            Node prev = node;
            node = node.parentNode();
            depth--;
            if (result == FilterResult.REMOVE)
                // Remove AFTER finding parent.
                prev.remove();
            // Parent was not pruned.
            result = FilterResult.CONTINUE;
        }
        // 'tail' current node, then proceed with siblings:
        if (result == FilterResult.CONTINUE || result == FilterResult.SKIP_CHILDREN) {
            result = filter.tail(node, depth);
            if (result == FilterResult.STOP)
                return result;
        }
        if (node == root)
            return result;
        // In case we need to remove it below.
        Node prev = node;
        node = node.nextSibling();
        if (result == FilterResult.REMOVE)
            // Remove AFTER finding sibling.
            prev.remove();
    }
    // root == null?
    return FilterResult.CONTINUE;
}
