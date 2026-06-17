output "public_ip" {
  value = aws_instance.k3s.public_ip
}
output "kubeconfig_note" {
  value = "scp ubuntu@${aws_instance.k3s.public_ip}:~/.kube/config ~/.kube/config"
}
