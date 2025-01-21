from moto import mock_iam, mock_ec2, mock_eks
import boto3
import unittest

class TestIAM(unittest.TestCase):

    @mock_iam
    def test_iam_roles(self):
        # Test IAM roles creation
        iam_client = boto3.client('iam', region_name='us-east-1')
        
        # Create mock IAM roles for EKS
        iam_client.create_role(
            RoleName='eks-role',
            AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"eks.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
        )
        
        iam_client.create_role(
            RoleName='node-role',
            AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
        )

        roles = iam_client.list_roles()['Roles']
        
        # Check that the roles are created
        self.assertEqual(len(roles), 2)  # eks-role and node-role should be created
        role_names = [role['RoleName'] for role in roles]
        self.assertIn('eks-role', role_names)
        self.assertIn('node-role', role_names)

    @mock_ec2
    def test_security_group(self):
        # Test EC2 security group creation
        ec2_client = boto3.client('ec2', region_name='us-east-1')

        # Create a mock security group
        response = ec2_client.create_security_group(
            GroupName='test-sg',
            Description='Test security group'
        )
        security_group_id = response['GroupId']

        # Get all security groups
        security_groups = ec2_client.describe_security_groups()['SecurityGroups']

        # Filter for the created security group by name
        test_security_groups = [sg for sg in security_groups if sg['GroupName'] == 'test-sg']

        # Check that only one security group matches the created group
        self.assertEqual(len(test_security_groups), 1)
        self.assertEqual(test_security_groups[0]['GroupName'], 'test-sg')
        self.assertEqual(test_security_groups[0]['GroupId'], security_group_id)

    @mock_eks
    @mock_ec2
    @mock_iam
    def test_eks_cluster(self):
        # Test EKS cluster creation
        eks_client = boto3.client('eks', region_name='us-east-1')
        iam_client = boto3.client('iam', region_name='us-east-1')
        ec2_client = boto3.client('ec2', region_name='us-east-1')

        # Mock VPC and Subnet
        vpc_response = ec2_client.create_vpc(CidrBlock='10.0.0.0/16')
        vpc_id = vpc_response['Vpc']['VpcId']
        subnet_response = ec2_client.create_subnet(CidrBlock='10.0.1.0/24', VpcId=vpc_id)
        subnet_id = subnet_response['Subnet']['SubnetId']

        # Create mock IAM roles for EKS
        eks_role = iam_client.create_role(
            RoleName='eks-role',
            AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"eks.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
        )
        
        node_role = iam_client.create_role(
            RoleName='node-role',
            AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
        )

        # Create EKS Cluster
        cluster_response = eks_client.create_cluster(
            name='flask-cluster',
            roleArn=eks_role['Role']['Arn'],
            resourcesVpcConfig={
                'subnetIds': [subnet_id],
                'securityGroupIds': []
            }
        )

        # Verify the EKS Cluster
        cluster = eks_client.describe_cluster(name='flask-cluster')['cluster']
        self.assertEqual(cluster['name'], 'flask-cluster')
        self.assertEqual(cluster['roleArn'], eks_role['Role']['Arn'])
        self.assertIn(subnet_id, cluster['resourcesVpcConfig']['subnetIds'])

if __name__ == '__main__':
    unittest.main()
