import { SharedArray } from 'k6/data';
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

const data = new SharedArray('terms', function () {
  const f = open('./query-terms.txt');
  return f.toString().split("\n");
});

export default function () {
  // Random query term, 50% likelyhood of 2 terms, 10% likelyhood of 3 terms
  let query = data[Math.floor(Math.random() * data.length)];
  if (Math.random() > 0.5) {
    query = query + ' ' + data[Math.floor(Math.random() * data.length)];
  }
  if (Math.random() > 0.9) {
    query = query + ' ' + data[Math.floor(Math.random() * data.length)];
  }
  console.log("Query is " + query);
  const res = http.get(`http://localhost:8983/solr/stackexchange/select?q.op=and&defType=dismax&qf=Title,Body&q=${query}`);
  check(res, { 'status was 200': (r) => r.status === 200 });
  sleep(1);
  // Add faceting
  http.get(`http://localhost:8983/solr/stackexchange/select?q=${query}&facet=true&facet.field=Tags`);
  sleep(1);
}