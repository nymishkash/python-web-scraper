#!/bin/bash
# Script to encode kubeconfig for GitHub Secrets

echo "=========================================="
echo "Kubeconfig Encoder for GitHub Secrets"
echo "=========================================="
echo ""
echo "Step 1: Paste your kubeconfig content below"
echo "        (Press Ctrl+D when done, or Ctrl+C to cancel)"
echo ""

# Read kubeconfig from stdin
cat > kubeconfig.yaml

echo ""
echo "Step 2: Encoding kubeconfig to base64..."
cat kubeconfig.yaml | base64 > kubeconfig.b64

echo "✅ Encoded kubeconfig saved to: kubeconfig.b64"
echo ""
echo "Step 3: Copy the content below and add to GitHub Secrets:"
echo "=========================================="
cat kubeconfig.b64
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy the encoded content above"
echo "2. Go to GitHub → Settings → Secrets → Actions"
echo "3. Add new secret: KUBE_CONFIG"
echo "4. Paste the encoded content"
echo ""
