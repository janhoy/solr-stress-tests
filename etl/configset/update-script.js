function processAdd(cmd) {
  doc = cmd.solrDoc;  // org.apache.solr.common.SolrInputDocument
  tags = doc.getField("Tags");
  // logger.info("Doc Before: " + doc);
  if (tags != null) {
    splitTags = tags.getFirstValue().replace(/^</, "").replace(/>$/, "").split("><");
    tags.setValue(null);
    splitTags.forEach(function(str) {
      tags.addValue(str);
    });
  }
  // logger.info("Doc after: " + doc);
}

function processDelete(cmd) {
  // no-op
}

function processMergeIndexes(cmd) {
  // no-op
}

function processCommit(cmd) {
  // no-op
}

function processRollback(cmd) {
  // no-op
}

function finish() {
  // no-op
}