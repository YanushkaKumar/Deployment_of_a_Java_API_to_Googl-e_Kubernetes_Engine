#!/bin/bash
echo "Cleaning up Java API deployment..."
kubectl delete -f k8s/ -n java-api-ns-yanushka
kubectl delete namespace java-api-ns-yanushka
echo "Cleanup complete."