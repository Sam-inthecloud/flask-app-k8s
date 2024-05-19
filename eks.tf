# EKS Cluster
resource "aws_eks_cluster" "flask_cluster" {
  name     = "flask-cluster"
  role_arn = aws_iam_role.eks_role.arn

  vpc_config {
    subnet_ids = aws_subnet.subnet_a[*].id
  }
  depends_on = [
    aws_iam_role_policy_attachment.eks_role_attachment
  ]
}

# EKS Node Group
resource "aws_eks_node_group" "flask_node_group" {
  cluster_name    = aws_eks_cluster.flask_cluster.name
  node_group_name = "flask-node-group"
  node_role_arn   = aws_iam_role.node_role.arn
  subnet_ids      = aws_subnet.subnet_a[*].id

  scaling_config {
    desired_size = 3
    max_size     = 4
    min_size     = 2
  }

instance_types = ["t3.medium"]

remote_access {
    ec2_ssh_key = "ec2-key"
    source_security_group_ids = [aws_security_group.eks_node_sg.id]
  }

 depends_on = [
    aws_eks_cluster.flask_cluster,
    aws_iam_role_policy_attachment.node_role_attachment,
    aws_iam_role_policy_attachment.node_role_cni_policy,
    aws_iam_role_policy_attachment.node_role_ec2_container_registry_read_only
  ]
tags = {
    Name = "flask-node-group"
  }
}


