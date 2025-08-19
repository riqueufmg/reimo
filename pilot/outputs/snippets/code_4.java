/**
 * Ensures a meta charset (html) or xml declaration (xml) with the current
 * encoding used. This only applies with
 * {@link #updateMetaCharsetElement(boolean) updateMetaCharset} set to
 * <tt>true</tt>, otherwise this method does nothing.
 *
 * <ul>
 * <li>An existing element gets updated with the current charset</li>
 * <li>If there's no element yet it will be inserted</li>
 * <li>Obsolete elements are removed</li>
 * </ul>
 *
 * <p><b>Elements used:</b></p>
 *
 * <ul>
 * <li><b>Html:</b> <i>&lt;meta charset="CHARSET"&gt;</i></li>
 * <li><b>Xml:</b> <i>&lt;?xml version="1.0" encoding="CHARSET"&gt;</i></li>
 * </ul>
 */
private void ensureMetaCharsetElement() {
    if (updateMetaCharset) {
        OutputSettings.Syntax syntax = outputSettings().syntax();
        if (syntax == OutputSettings.Syntax.html) {
            Element metaCharset = selectFirst("meta[charset]");
            if (metaCharset != null) {
                metaCharset.attr("charset", charset().displayName());
            } else {
                head().appendElement("meta").attr("charset", charset().displayName());
            }
            // Remove obsolete elements
            select("meta[name=charset]").remove();
        } else if (syntax == OutputSettings.Syntax.xml) {
            Node node = ensureChildNodes().get(0);
            if (node instanceof XmlDeclaration) {
                XmlDeclaration decl = (XmlDeclaration) node;
                if (decl.name().equals("xml")) {
                    decl.attr("encoding", charset().displayName());
                    if (decl.hasAttr("version"))
                        decl.attr("version", "1.0");
                } else {
                    decl = new XmlDeclaration("xml", false);
                    decl.attr("version", "1.0");
                    decl.attr("encoding", charset().displayName());
                    prependChild(decl);
                }
            } else {
                XmlDeclaration decl = new XmlDeclaration("xml", false);
                decl.attr("version", "1.0");
                decl.attr("encoding", charset().displayName());
                prependChild(decl);
            }
        }
    }
}
