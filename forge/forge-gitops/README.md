# Forge desired state

Chart comun în `charts/forge-service`, valori în `environments/{dev,prod}`.
Bootstrap dev în `bootstrap`. Argo CD trebuie instalat separat.

`helm lint charts/forge-service` și `helm template demo charts/forge-service`.
Image digest are prioritate față de tag. Folosește digest pentru deployment AWS.
HPA necesită Metrics Server. ServiceMonitor/PrometheusRule necesită Prometheus
Operator. NetworkPolicy necesită un CNI care aplică policy; kind implicit nu este
o demonstrație de enforce. Egress empty blochează inclusiv DNS dacă policy este
activată, intenționat pentru serviciul demo care nu are dependențe externe.

Nu activa monitoring/policy fără dependențele respective și verificări în cluster.
Nu comite token-uri sau secrete în GitOps. Argo project limitează destinația la
forge-dev și nu acordă permisiuni pentru resurse cluster-wide.
