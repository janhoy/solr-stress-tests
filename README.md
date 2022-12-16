# Stress tests for Solr in k8s

This repo uses [k6](https://k6.io) to load test a Solr cluster.

## Data

The test will download a [sample dataset](https://archive.org/details/stackexchange) from StackExchange on the topic 'cooking'.
The archive is unzipped, and 122540 posts are indexed from Posts.xml, into a Solr collection with a schema that follows
the [data format](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede)
of the data.

## Tests

The first test is creating a config set with the schema, and then a collection with two replicas.

Then, we run an indexing test which indexes the data and measures time.

Finally, we have various query load tests.

## Rest results

Results of the tests are available as a summary, and as more detailed data.

## Running locally

```bash
# Install k6
brew install k6

cd tests
k6 run k6-test.js
```
