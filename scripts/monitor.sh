#!/bin/bash
echo "==== Java API Monitoring ===="
echo "Namespace: java-api-ns-yanushka"
echo
echo "Pods Status:"
kubectl get pods -n java-api-ns-yanushka
echo
echo "Service Status:"
kubectl get svc -n java-api-ns-yanushka
echo
echo "Ingress Status:"
kubectl get ingress -n java-api-ns-yanushka
echo
echo "HPA Status:"
kubectl get hpa -n java-api-ns-yanushka
echo
echo "Recent Events:"
kubectl get events -n java-api-ns-yanushka --sort-by=.metadata.creationTimestamp | tail -10