#!/usr/bin/env python3

import boto3

# Add to the region list as you see fit.
# The for loop is describing all EC2 instances in that particular account, filtering for the
# instance type name (i.e., M5.large C6a.2xlarge, c6g.large). Everything not AMD or Intel are
# grouped as other.

# Regions
regions = ["us-east-1", "us-east-2"]

amdtype = ["m7a", "m6a", "m5a", "t3a"]
inteltype = ["m7i", "m6i", "m5", "m4", "t3"]
othertype = ["mac1", "mac2", "m7g", "m6g", "t3g"]

for region in regions:
    # Initialize Boto3 client for EC2 in the specified region
    ec2_client = boto3.client("ec2", region_name=region)

    # Gather all instances per region
    response = ec2_client.describe_instances()
    instances = [instance["InstanceType"] for reservation in response["Reservations"] for instance in reservation["Instances"]]

    # AMD scan
    amd_instances = sum(1 for instance in instances if any(type in instance for type in amdtype))

    # Intel scan
    intel_instances = sum(1 for instance in instances if any(instance.startswith(type) for type in inteltype))

    # Other scan
    other_instances = sum(1 for instance in instances if all(type not in instance for type in amdtype + inteltype))

    # Table
    print("%-15s %-15s %-15s %-15s" % ("Region", "AMD Instances", "Intel Instances", "Other Types"))
    print("------------------------------------------------------------------------------------")
    # Data
    print("%-15s %-15s %-15s %-15s" % (region, amd_instances, intel_instances, other_instances))

