import logging
import sys
from typing import Any, Optional, Union, overload

from boto3 import session as session
from boto3.session import Session as Session
from botocore.config import Config
from botocore.session import Session as BotocoreSession
from mypy_boto3_accessanalyzer.client import AccessAnalyzerClient
from mypy_boto3_account.client import AccountClient
from mypy_boto3_acm.client import ACMClient
from mypy_boto3_acm_pca.client import ACMPCAClient
from mypy_boto3_amp.client import PrometheusServiceClient
from mypy_boto3_amplify.client import AmplifyClient
from mypy_boto3_amplifybackend.client import AmplifyBackendClient
from mypy_boto3_amplifyuibuilder.client import AmplifyUIBuilderClient
from mypy_boto3_apigateway.client import APIGatewayClient
from mypy_boto3_apigatewaymanagementapi.client import ApiGatewayManagementApiClient
from mypy_boto3_apigatewayv2.client import ApiGatewayV2Client
from mypy_boto3_appconfig.client import AppConfigClient
from mypy_boto3_appconfigdata.client import AppConfigDataClient
from mypy_boto3_appfabric.client import AppFabricClient
from mypy_boto3_appflow.client import AppflowClient
from mypy_boto3_appintegrations.client import AppIntegrationsServiceClient
from mypy_boto3_application_autoscaling.client import ApplicationAutoScalingClient
from mypy_boto3_application_insights.client import ApplicationInsightsClient
from mypy_boto3_application_signals.client import CloudWatchApplicationSignalsClient
from mypy_boto3_applicationcostprofiler.client import ApplicationCostProfilerClient
from mypy_boto3_appmesh.client import AppMeshClient
from mypy_boto3_apprunner.client import AppRunnerClient
from mypy_boto3_appstream.client import AppStreamClient
from mypy_boto3_appsync.client import AppSyncClient
from mypy_boto3_apptest.client import MainframeModernizationApplicationTestingClient
from mypy_boto3_arc_zonal_shift.client import ARCZonalShiftClient
from mypy_boto3_artifact.client import ArtifactClient
from mypy_boto3_athena.client import AthenaClient
from mypy_boto3_auditmanager.client import AuditManagerClient
from mypy_boto3_autoscaling.client import AutoScalingClient
from mypy_boto3_autoscaling_plans.client import AutoScalingPlansClient
from mypy_boto3_b2bi.client import B2BIClient
from mypy_boto3_backup.client import BackupClient
from mypy_boto3_backup_gateway.client import BackupGatewayClient
from mypy_boto3_batch.client import BatchClient
from mypy_boto3_bcm_data_exports.client import BillingandCostManagementDataExportsClient
from mypy_boto3_bedrock.client import BedrockClient
from mypy_boto3_bedrock_agent.client import AgentsforBedrockClient
from mypy_boto3_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
from mypy_boto3_bedrock_runtime.client import BedrockRuntimeClient
from mypy_boto3_billingconductor.client import BillingConductorClient
from mypy_boto3_braket.client import BraketClient
from mypy_boto3_budgets.client import BudgetsClient
from mypy_boto3_ce.client import CostExplorerClient
from mypy_boto3_chatbot.client import ChatbotClient
from mypy_boto3_chime.client import ChimeClient
from mypy_boto3_chime_sdk_identity.client import ChimeSDKIdentityClient
from mypy_boto3_chime_sdk_media_pipelines.client import ChimeSDKMediaPipelinesClient
from mypy_boto3_chime_sdk_meetings.client import ChimeSDKMeetingsClient
from mypy_boto3_chime_sdk_messaging.client import ChimeSDKMessagingClient
from mypy_boto3_chime_sdk_voice.client import ChimeSDKVoiceClient
from mypy_boto3_cleanrooms.client import CleanRoomsServiceClient
from mypy_boto3_cleanroomsml.client import CleanRoomsMLClient
from mypy_boto3_cloud9.client import Cloud9Client
from mypy_boto3_cloudcontrol.client import CloudControlApiClient
from mypy_boto3_clouddirectory.client import CloudDirectoryClient
from mypy_boto3_cloudformation.client import CloudFormationClient
from mypy_boto3_cloudformation.service_resource import CloudFormationServiceResource
from mypy_boto3_cloudfront.client import CloudFrontClient
from mypy_boto3_cloudfront_keyvaluestore.client import CloudFrontKeyValueStoreClient
from mypy_boto3_cloudhsm.client import CloudHSMClient
from mypy_boto3_cloudhsmv2.client import CloudHSMV2Client
from mypy_boto3_cloudsearch.client import CloudSearchClient
from mypy_boto3_cloudsearchdomain.client import CloudSearchDomainClient
from mypy_boto3_cloudtrail.client import CloudTrailClient
from mypy_boto3_cloudtrail_data.client import CloudTrailDataServiceClient
from mypy_boto3_cloudwatch.client import CloudWatchClient
from mypy_boto3_cloudwatch.service_resource import CloudWatchServiceResource
from mypy_boto3_codeartifact.client import CodeArtifactClient
from mypy_boto3_codebuild.client import CodeBuildClient
from mypy_boto3_codecatalyst.client import CodeCatalystClient
from mypy_boto3_codecommit.client import CodeCommitClient
from mypy_boto3_codeconnections.client import CodeConnectionsClient
from mypy_boto3_codedeploy.client import CodeDeployClient
from mypy_boto3_codeguru_reviewer.client import CodeGuruReviewerClient
from mypy_boto3_codeguru_security.client import CodeGuruSecurityClient
from mypy_boto3_codeguruprofiler.client import CodeGuruProfilerClient
from mypy_boto3_codepipeline.client import CodePipelineClient
from mypy_boto3_codestar.client import CodeStarClient
from mypy_boto3_codestar_connections.client import CodeStarconnectionsClient
from mypy_boto3_codestar_notifications.client import CodeStarNotificationsClient
from mypy_boto3_cognito_identity.client import CognitoIdentityClient
from mypy_boto3_cognito_idp.client import CognitoIdentityProviderClient
from mypy_boto3_cognito_sync.client import CognitoSyncClient
from mypy_boto3_comprehend.client import ComprehendClient
from mypy_boto3_comprehendmedical.client import ComprehendMedicalClient
from mypy_boto3_compute_optimizer.client import ComputeOptimizerClient
from mypy_boto3_config.client import ConfigServiceClient
from mypy_boto3_connect.client import ConnectClient
from mypy_boto3_connect_contact_lens.client import ConnectContactLensClient
from mypy_boto3_connectcampaigns.client import ConnectCampaignServiceClient
from mypy_boto3_connectcases.client import ConnectCasesClient
from mypy_boto3_connectparticipant.client import ConnectParticipantClient
from mypy_boto3_controlcatalog.client import ControlCatalogClient
from mypy_boto3_controltower.client import ControlTowerClient
from mypy_boto3_cost_optimization_hub.client import CostOptimizationHubClient
from mypy_boto3_cur.client import CostandUsageReportServiceClient
from mypy_boto3_customer_profiles.client import CustomerProfilesClient
from mypy_boto3_databrew.client import GlueDataBrewClient
from mypy_boto3_dataexchange.client import DataExchangeClient
from mypy_boto3_datapipeline.client import DataPipelineClient
from mypy_boto3_datasync.client import DataSyncClient
from mypy_boto3_datazone.client import DataZoneClient
from mypy_boto3_dax.client import DAXClient
from mypy_boto3_deadline.client import DeadlineCloudClient
from mypy_boto3_detective.client import DetectiveClient
from mypy_boto3_devicefarm.client import DeviceFarmClient
from mypy_boto3_devops_guru.client import DevOpsGuruClient
from mypy_boto3_directconnect.client import DirectConnectClient
from mypy_boto3_discovery.client import ApplicationDiscoveryServiceClient
from mypy_boto3_dlm.client import DLMClient
from mypy_boto3_dms.client import DatabaseMigrationServiceClient
from mypy_boto3_docdb.client import DocDBClient
from mypy_boto3_docdb_elastic.client import DocDBElasticClient
from mypy_boto3_drs.client import DrsClient
from mypy_boto3_ds.client import DirectoryServiceClient
from mypy_boto3_dynamodb.client import DynamoDBClient
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
from mypy_boto3_dynamodbstreams.client import DynamoDBStreamsClient
from mypy_boto3_ebs.client import EBSClient
from mypy_boto3_ec2.client import EC2Client
from mypy_boto3_ec2.service_resource import EC2ServiceResource
from mypy_boto3_ec2_instance_connect.client import EC2InstanceConnectClient
from mypy_boto3_ecr.client import ECRClient
from mypy_boto3_ecr_public.client import ECRPublicClient
from mypy_boto3_ecs.client import ECSClient
from mypy_boto3_efs.client import EFSClient
from mypy_boto3_eks.client import EKSClient
from mypy_boto3_eks_auth.client import EKSAuthClient
from mypy_boto3_elastic_inference.client import ElasticInferenceClient
from mypy_boto3_elasticache.client import ElastiCacheClient
from mypy_boto3_elasticbeanstalk.client import ElasticBeanstalkClient
from mypy_boto3_elastictranscoder.client import ElasticTranscoderClient
from mypy_boto3_elb.client import ElasticLoadBalancingClient
from mypy_boto3_elbv2.client import ElasticLoadBalancingv2Client
from mypy_boto3_emr.client import EMRClient
from mypy_boto3_emr_containers.client import EMRContainersClient
from mypy_boto3_emr_serverless.client import EMRServerlessClient
from mypy_boto3_entityresolution.client import EntityResolutionClient
from mypy_boto3_es.client import ElasticsearchServiceClient
from mypy_boto3_events.client import EventBridgeClient
from mypy_boto3_evidently.client import CloudWatchEvidentlyClient
from mypy_boto3_finspace.client import FinspaceClient
from mypy_boto3_finspace_data.client import FinSpaceDataClient
from mypy_boto3_firehose.client import FirehoseClient
from mypy_boto3_fis.client import FISClient
from mypy_boto3_fms.client import FMSClient
from mypy_boto3_forecast.client import ForecastServiceClient
from mypy_boto3_forecastquery.client import ForecastQueryServiceClient
from mypy_boto3_frauddetector.client import FraudDetectorClient
from mypy_boto3_freetier.client import FreeTierClient
from mypy_boto3_fsx.client import FSxClient
from mypy_boto3_gamelift.client import GameLiftClient
from mypy_boto3_glacier.client import GlacierClient
from mypy_boto3_glacier.service_resource import GlacierServiceResource
from mypy_boto3_globalaccelerator.client import GlobalAcceleratorClient
from mypy_boto3_glue.client import GlueClient
from mypy_boto3_grafana.client import ManagedGrafanaClient
from mypy_boto3_greengrass.client import GreengrassClient
from mypy_boto3_greengrassv2.client import GreengrassV2Client
from mypy_boto3_groundstation.client import GroundStationClient
from mypy_boto3_guardduty.client import GuardDutyClient
from mypy_boto3_health.client import HealthClient
from mypy_boto3_healthlake.client import HealthLakeClient
from mypy_boto3_iam.client import IAMClient
from mypy_boto3_iam.service_resource import IAMServiceResource
from mypy_boto3_identitystore.client import IdentityStoreClient
from mypy_boto3_imagebuilder.client import ImagebuilderClient
from mypy_boto3_importexport.client import ImportExportClient
from mypy_boto3_inspector2.client import Inspector2Client
from mypy_boto3_inspector.client import InspectorClient
from mypy_boto3_inspector_scan.client import InspectorscanClient
from mypy_boto3_internetmonitor.client import CloudWatchInternetMonitorClient
from mypy_boto3_iot1click_devices.client import IoT1ClickDevicesServiceClient
from mypy_boto3_iot1click_projects.client import IoT1ClickProjectsClient
from mypy_boto3_iot.client import IoTClient
from mypy_boto3_iot_data.client import IoTDataPlaneClient
from mypy_boto3_iot_jobs_data.client import IoTJobsDataPlaneClient
from mypy_boto3_iotanalytics.client import IoTAnalyticsClient
from mypy_boto3_iotdeviceadvisor.client import IoTDeviceAdvisorClient
from mypy_boto3_iotevents.client import IoTEventsClient
from mypy_boto3_iotevents_data.client import IoTEventsDataClient
from mypy_boto3_iotfleethub.client import IoTFleetHubClient
from mypy_boto3_iotfleetwise.client import IoTFleetWiseClient
from mypy_boto3_iotsecuretunneling.client import IoTSecureTunnelingClient
from mypy_boto3_iotsitewise.client import IoTSiteWiseClient
from mypy_boto3_iotthingsgraph.client import IoTThingsGraphClient
from mypy_boto3_iottwinmaker.client import IoTTwinMakerClient
from mypy_boto3_iotwireless.client import IoTWirelessClient
from mypy_boto3_ivs.client import IVSClient
from mypy_boto3_ivs_realtime.client import IvsrealtimeClient
from mypy_boto3_ivschat.client import IvschatClient
from mypy_boto3_kafka.client import KafkaClient
from mypy_boto3_kafkaconnect.client import KafkaConnectClient
from mypy_boto3_kendra.client import KendraClient
from mypy_boto3_kendra_ranking.client import KendraRankingClient
from mypy_boto3_keyspaces.client import KeyspacesClient
from mypy_boto3_kinesis.client import KinesisClient
from mypy_boto3_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient
from mypy_boto3_kinesis_video_media.client import KinesisVideoMediaClient
from mypy_boto3_kinesis_video_signaling.client import KinesisVideoSignalingChannelsClient
from mypy_boto3_kinesis_video_webrtc_storage.client import KinesisVideoWebRTCStorageClient
from mypy_boto3_kinesisanalytics.client import KinesisAnalyticsClient
from mypy_boto3_kinesisanalyticsv2.client import KinesisAnalyticsV2Client
from mypy_boto3_kinesisvideo.client import KinesisVideoClient
from mypy_boto3_kms.client import KMSClient
from mypy_boto3_lakeformation.client import LakeFormationClient
from mypy_boto3_lambda.client import LambdaClient
from mypy_boto3_launch_wizard.client import LaunchWizardClient
from mypy_boto3_lex_models.client import LexModelBuildingServiceClient
from mypy_boto3_lex_runtime.client import LexRuntimeServiceClient
from mypy_boto3_lexv2_models.client import LexModelsV2Client
from mypy_boto3_lexv2_runtime.client import LexRuntimeV2Client
from mypy_boto3_license_manager.client import LicenseManagerClient
from mypy_boto3_license_manager_linux_subscriptions.client import (
    LicenseManagerLinuxSubscriptionsClient,
)
from mypy_boto3_license_manager_user_subscriptions.client import (
    LicenseManagerUserSubscriptionsClient,
)
from mypy_boto3_lightsail.client import LightsailClient
from mypy_boto3_location.client import LocationServiceClient
from mypy_boto3_logs.client import CloudWatchLogsClient
from mypy_boto3_lookoutequipment.client import LookoutEquipmentClient
from mypy_boto3_lookoutmetrics.client import LookoutMetricsClient
from mypy_boto3_lookoutvision.client import LookoutforVisionClient
from mypy_boto3_m2.client import MainframeModernizationClient
from mypy_boto3_machinelearning.client import MachineLearningClient
from mypy_boto3_macie2.client import Macie2Client
from mypy_boto3_mailmanager.client import MailManagerClient
from mypy_boto3_managedblockchain.client import ManagedBlockchainClient
from mypy_boto3_managedblockchain_query.client import ManagedBlockchainQueryClient
from mypy_boto3_marketplace_agreement.client import AgreementServiceClient
from mypy_boto3_marketplace_catalog.client import MarketplaceCatalogClient
from mypy_boto3_marketplace_deployment.client import MarketplaceDeploymentServiceClient
from mypy_boto3_marketplace_entitlement.client import MarketplaceEntitlementServiceClient
from mypy_boto3_marketplacecommerceanalytics.client import MarketplaceCommerceAnalyticsClient
from mypy_boto3_mediaconnect.client import MediaConnectClient
from mypy_boto3_mediaconvert.client import MediaConvertClient
from mypy_boto3_medialive.client import MediaLiveClient
from mypy_boto3_mediapackage.client import MediaPackageClient
from mypy_boto3_mediapackage_vod.client import MediaPackageVodClient
from mypy_boto3_mediapackagev2.client import Mediapackagev2Client
from mypy_boto3_mediastore.client import MediaStoreClient
from mypy_boto3_mediastore_data.client import MediaStoreDataClient
from mypy_boto3_mediatailor.client import MediaTailorClient
from mypy_boto3_medical_imaging.client import HealthImagingClient
from mypy_boto3_memorydb.client import MemoryDBClient
from mypy_boto3_meteringmarketplace.client import MarketplaceMeteringClient
from mypy_boto3_mgh.client import MigrationHubClient
from mypy_boto3_mgn.client import MgnClient
from mypy_boto3_migration_hub_refactor_spaces.client import MigrationHubRefactorSpacesClient
from mypy_boto3_migrationhub_config.client import MigrationHubConfigClient
from mypy_boto3_migrationhuborchestrator.client import MigrationHubOrchestratorClient
from mypy_boto3_migrationhubstrategy.client import MigrationHubStrategyRecommendationsClient
from mypy_boto3_mobile.client import MobileClient
from mypy_boto3_mq.client import MQClient
from mypy_boto3_mturk.client import MTurkClient
from mypy_boto3_mwaa.client import MWAAClient
from mypy_boto3_neptune.client import NeptuneClient
from mypy_boto3_neptune_graph.client import NeptuneGraphClient
from mypy_boto3_neptunedata.client import NeptuneDataClient
from mypy_boto3_network_firewall.client import NetworkFirewallClient
from mypy_boto3_networkmanager.client import NetworkManagerClient
from mypy_boto3_networkmonitor.client import CloudWatchNetworkMonitorClient
from mypy_boto3_nimble.client import NimbleStudioClient
from mypy_boto3_oam.client import CloudWatchObservabilityAccessManagerClient
from mypy_boto3_omics.client import OmicsClient
from mypy_boto3_opensearch.client import OpenSearchServiceClient
from mypy_boto3_opensearchserverless.client import OpenSearchServiceServerlessClient
from mypy_boto3_opsworks.client import OpsWorksClient
from mypy_boto3_opsworks.service_resource import OpsWorksServiceResource
from mypy_boto3_opsworkscm.client import OpsWorksCMClient
from mypy_boto3_organizations.client import OrganizationsClient
from mypy_boto3_osis.client import OpenSearchIngestionClient
from mypy_boto3_outposts.client import OutpostsClient
from mypy_boto3_panorama.client import PanoramaClient
from mypy_boto3_payment_cryptography.client import PaymentCryptographyControlPlaneClient
from mypy_boto3_payment_cryptography_data.client import PaymentCryptographyDataPlaneClient
from mypy_boto3_pca_connector_ad.client import PcaConnectorAdClient
from mypy_boto3_pca_connector_scep.client import PrivateCAConnectorforSCEPClient
from mypy_boto3_personalize.client import PersonalizeClient
from mypy_boto3_personalize_events.client import PersonalizeEventsClient
from mypy_boto3_personalize_runtime.client import PersonalizeRuntimeClient
from mypy_boto3_pi.client import PIClient
from mypy_boto3_pinpoint.client import PinpointClient
from mypy_boto3_pinpoint_email.client import PinpointEmailClient
from mypy_boto3_pinpoint_sms_voice.client import PinpointSMSVoiceClient
from mypy_boto3_pinpoint_sms_voice_v2.client import PinpointSMSVoiceV2Client
from mypy_boto3_pipes.client import EventBridgePipesClient
from mypy_boto3_polly.client import PollyClient
from mypy_boto3_pricing.client import PricingClient
from mypy_boto3_privatenetworks.client import Private5GClient
from mypy_boto3_proton.client import ProtonClient
from mypy_boto3_qbusiness.client import QBusinessClient
from mypy_boto3_qconnect.client import QConnectClient
from mypy_boto3_qldb.client import QLDBClient
from mypy_boto3_qldb_session.client import QLDBSessionClient
from mypy_boto3_quicksight.client import QuickSightClient
from mypy_boto3_ram.client import RAMClient
from mypy_boto3_rbin.client import RecycleBinClient
from mypy_boto3_rds.client import RDSClient
from mypy_boto3_rds_data.client import RDSDataServiceClient
from mypy_boto3_redshift.client import RedshiftClient
from mypy_boto3_redshift_data.client import RedshiftDataAPIServiceClient
from mypy_boto3_redshift_serverless.client import RedshiftServerlessClient
from mypy_boto3_rekognition.client import RekognitionClient
from mypy_boto3_repostspace.client import RePostPrivateClient
from mypy_boto3_resiliencehub.client import ResilienceHubClient
from mypy_boto3_resource_explorer_2.client import ResourceExplorerClient
from mypy_boto3_resource_groups.client import ResourceGroupsClient
from mypy_boto3_resourcegroupstaggingapi.client import ResourceGroupsTaggingAPIClient
from mypy_boto3_robomaker.client import RoboMakerClient
from mypy_boto3_rolesanywhere.client import IAMRolesAnywhereClient
from mypy_boto3_route53.client import Route53Client
from mypy_boto3_route53_recovery_cluster.client import Route53RecoveryClusterClient
from mypy_boto3_route53_recovery_control_config.client import Route53RecoveryControlConfigClient
from mypy_boto3_route53_recovery_readiness.client import Route53RecoveryReadinessClient
from mypy_boto3_route53domains.client import Route53DomainsClient
from mypy_boto3_route53profiles.client import Route53ProfilesClient
from mypy_boto3_route53resolver.client import Route53ResolverClient
from mypy_boto3_rum.client import CloudWatchRUMClient
from mypy_boto3_s3.client import S3Client
from mypy_boto3_s3.service_resource import S3ServiceResource
from mypy_boto3_s3control.client import S3ControlClient
from mypy_boto3_s3outposts.client import S3OutpostsClient
from mypy_boto3_sagemaker.client import SageMakerClient
from mypy_boto3_sagemaker_a2i_runtime.client import AugmentedAIRuntimeClient
from mypy_boto3_sagemaker_edge.client import SagemakerEdgeManagerClient
from mypy_boto3_sagemaker_featurestore_runtime.client import SageMakerFeatureStoreRuntimeClient
from mypy_boto3_sagemaker_geospatial.client import SageMakergeospatialcapabilitiesClient
from mypy_boto3_sagemaker_metrics.client import SageMakerMetricsClient
from mypy_boto3_sagemaker_runtime.client import SageMakerRuntimeClient
from mypy_boto3_savingsplans.client import SavingsPlansClient
from mypy_boto3_scheduler.client import EventBridgeSchedulerClient
from mypy_boto3_schemas.client import SchemasClient
from mypy_boto3_sdb.client import SimpleDBClient
from mypy_boto3_secretsmanager.client import SecretsManagerClient
from mypy_boto3_securityhub.client import SecurityHubClient
from mypy_boto3_securitylake.client import SecurityLakeClient
from mypy_boto3_serverlessrepo.client import ServerlessApplicationRepositoryClient
from mypy_boto3_service_quotas.client import ServiceQuotasClient
from mypy_boto3_servicecatalog.client import ServiceCatalogClient
from mypy_boto3_servicecatalog_appregistry.client import AppRegistryClient
from mypy_boto3_servicediscovery.client import ServiceDiscoveryClient
from mypy_boto3_ses.client import SESClient
from mypy_boto3_sesv2.client import SESV2Client
from mypy_boto3_shield.client import ShieldClient
from mypy_boto3_signer.client import SignerClient
from mypy_boto3_simspaceweaver.client import SimSpaceWeaverClient
from mypy_boto3_sms.client import SMSClient
from mypy_boto3_sms_voice.client import PinpointSMSVoiceClient
from mypy_boto3_snow_device_management.client import SnowDeviceManagementClient
from mypy_boto3_snowball.client import SnowballClient
from mypy_boto3_sns.client import SNSClient
from mypy_boto3_sns.service_resource import SNSServiceResource
from mypy_boto3_sqs.client import SQSClient
from mypy_boto3_sqs.service_resource import SQSServiceResource
from mypy_boto3_ssm.client import SSMClient
from mypy_boto3_ssm_contacts.client import SSMContactsClient
from mypy_boto3_ssm_incidents.client import SSMIncidentsClient
from mypy_boto3_ssm_sap.client import SsmSapClient
from mypy_boto3_sso.client import SSOClient
from mypy_boto3_sso_admin.client import SSOAdminClient
from mypy_boto3_sso_oidc.client import SSOOIDCClient
from mypy_boto3_stepfunctions.client import SFNClient
from mypy_boto3_storagegateway.client import StorageGatewayClient
from mypy_boto3_sts.client import STSClient
from mypy_boto3_supplychain.client import SupplyChainClient
from mypy_boto3_support.client import SupportClient
from mypy_boto3_support_app.client import SupportAppClient
from mypy_boto3_swf.client import SWFClient
from mypy_boto3_synthetics.client import SyntheticsClient
from mypy_boto3_taxsettings.client import TaxSettingsClient
from mypy_boto3_textract.client import TextractClient
from mypy_boto3_timestream_influxdb.client import TimestreamInfluxDBClient
from mypy_boto3_timestream_query.client import TimestreamQueryClient
from mypy_boto3_timestream_write.client import TimestreamWriteClient
from mypy_boto3_tnb.client import TelcoNetworkBuilderClient
from mypy_boto3_transcribe.client import TranscribeServiceClient
from mypy_boto3_transfer.client import TransferClient
from mypy_boto3_translate.client import TranslateClient
from mypy_boto3_trustedadvisor.client import TrustedAdvisorPublicAPIClient
from mypy_boto3_verifiedpermissions.client import VerifiedPermissionsClient
from mypy_boto3_voice_id.client import VoiceIDClient
from mypy_boto3_vpc_lattice.client import VPCLatticeClient
from mypy_boto3_waf.client import WAFClient
from mypy_boto3_waf_regional.client import WAFRegionalClient
from mypy_boto3_wafv2.client import WAFV2Client
from mypy_boto3_wellarchitected.client import WellArchitectedClient
from mypy_boto3_wisdom.client import ConnectWisdomServiceClient
from mypy_boto3_workdocs.client import WorkDocsClient
from mypy_boto3_worklink.client import WorkLinkClient
from mypy_boto3_workmail.client import WorkMailClient
from mypy_boto3_workmailmessageflow.client import WorkMailMessageFlowClient
from mypy_boto3_workspaces.client import WorkSpacesClient
from mypy_boto3_workspaces_thin_client.client import WorkSpacesThinClientClient
from mypy_boto3_workspaces_web.client import WorkSpacesWebClient
from mypy_boto3_xray.client import XRayClient

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
__author__: str
__version__: str

DEFAULT_SESSION: Optional[Session]

def setup_default_session(
    *,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    region_name: Optional[str] = ...,
    botocore_session: Optional[BotocoreSession] = ...,
    profile_name: Optional[str] = ...,
) -> None: ...
def set_stream_logger(
    name: str = ..., level: int = ..., format_string: Optional[str] = ...
) -> None: ...
def _get_default_session() -> Session: ...

class NullHandler(logging.Handler):
    def emit(self, record: Any) -> Any: ...

@overload
def client(
    service_name: Literal["accessanalyzer"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AccessAnalyzerClient: ...
@overload
def client(
    service_name: Literal["account"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AccountClient: ...
@overload
def client(
    service_name: Literal["acm"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ACMClient: ...
@overload
def client(
    service_name: Literal["acm-pca"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ACMPCAClient: ...
@overload
def client(
    service_name: Literal["amp"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PrometheusServiceClient: ...
@overload
def client(
    service_name: Literal["amplify"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AmplifyClient: ...
@overload
def client(
    service_name: Literal["amplifybackend"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AmplifyBackendClient: ...
@overload
def client(
    service_name: Literal["amplifyuibuilder"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AmplifyUIBuilderClient: ...
@overload
def client(
    service_name: Literal["apigateway"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> APIGatewayClient: ...
@overload
def client(
    service_name: Literal["apigatewaymanagementapi"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ApiGatewayManagementApiClient: ...
@overload
def client(
    service_name: Literal["apigatewayv2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ApiGatewayV2Client: ...
@overload
def client(
    service_name: Literal["appconfig"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AppConfigClient: ...
@overload
def client(
    service_name: Literal["appconfigdata"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AppConfigDataClient: ...
@overload
def client(
    service_name: Literal["appfabric"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AppFabricClient: ...
@overload
def client(
    service_name: Literal["appflow"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AppflowClient: ...
@overload
def client(
    service_name: Literal["appintegrations"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AppIntegrationsServiceClient: ...
@overload
def client(
    service_name: Literal["application-autoscaling"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ApplicationAutoScalingClient: ...
@overload
def client(
    service_name: Literal["application-insights"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ApplicationInsightsClient: ...
@overload
def client(
    service_name: Literal["application-signals"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudWatchApplicationSignalsClient: ...
@overload
def client(
    service_name: Literal["applicationcostprofiler"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ApplicationCostProfilerClient: ...
@overload
def client(
    service_name: Literal["appmesh"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AppMeshClient: ...
@overload
def client(
    service_name: Literal["apprunner"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AppRunnerClient: ...
@overload
def client(
    service_name: Literal["appstream"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AppStreamClient: ...
@overload
def client(
    service_name: Literal["appsync"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AppSyncClient: ...
@overload
def client(
    service_name: Literal["apptest"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MainframeModernizationApplicationTestingClient: ...
@overload
def client(
    service_name: Literal["arc-zonal-shift"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ARCZonalShiftClient: ...
@overload
def client(
    service_name: Literal["artifact"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ArtifactClient: ...
@overload
def client(
    service_name: Literal["athena"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AthenaClient: ...
@overload
def client(
    service_name: Literal["auditmanager"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AuditManagerClient: ...
@overload
def client(
    service_name: Literal["autoscaling"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AutoScalingClient: ...
@overload
def client(
    service_name: Literal["autoscaling-plans"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AutoScalingPlansClient: ...
@overload
def client(
    service_name: Literal["b2bi"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> B2BIClient: ...
@overload
def client(
    service_name: Literal["backup"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> BackupClient: ...
@overload
def client(
    service_name: Literal["backup-gateway"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> BackupGatewayClient: ...
@overload
def client(
    service_name: Literal["batch"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> BatchClient: ...
@overload
def client(
    service_name: Literal["bcm-data-exports"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> BillingandCostManagementDataExportsClient: ...
@overload
def client(
    service_name: Literal["bedrock"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> BedrockClient: ...
@overload
def client(
    service_name: Literal["bedrock-agent"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AgentsforBedrockClient: ...
@overload
def client(
    service_name: Literal["bedrock-agent-runtime"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AgentsforBedrockRuntimeClient: ...
@overload
def client(
    service_name: Literal["bedrock-runtime"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> BedrockRuntimeClient: ...
@overload
def client(
    service_name: Literal["billingconductor"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> BillingConductorClient: ...
@overload
def client(
    service_name: Literal["braket"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> BraketClient: ...
@overload
def client(
    service_name: Literal["budgets"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> BudgetsClient: ...
@overload
def client(
    service_name: Literal["ce"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CostExplorerClient: ...
@overload
def client(
    service_name: Literal["chatbot"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ChatbotClient: ...
@overload
def client(
    service_name: Literal["chime"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ChimeClient: ...
@overload
def client(
    service_name: Literal["chime-sdk-identity"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ChimeSDKIdentityClient: ...
@overload
def client(
    service_name: Literal["chime-sdk-media-pipelines"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ChimeSDKMediaPipelinesClient: ...
@overload
def client(
    service_name: Literal["chime-sdk-meetings"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ChimeSDKMeetingsClient: ...
@overload
def client(
    service_name: Literal["chime-sdk-messaging"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ChimeSDKMessagingClient: ...
@overload
def client(
    service_name: Literal["chime-sdk-voice"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ChimeSDKVoiceClient: ...
@overload
def client(
    service_name: Literal["cleanrooms"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CleanRoomsServiceClient: ...
@overload
def client(
    service_name: Literal["cleanroomsml"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CleanRoomsMLClient: ...
@overload
def client(
    service_name: Literal["cloud9"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Cloud9Client: ...
@overload
def client(
    service_name: Literal["cloudcontrol"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudControlApiClient: ...
@overload
def client(
    service_name: Literal["clouddirectory"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudDirectoryClient: ...
@overload
def client(
    service_name: Literal["cloudformation"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudFormationClient: ...
@overload
def client(
    service_name: Literal["cloudfront"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudFrontClient: ...
@overload
def client(
    service_name: Literal["cloudfront-keyvaluestore"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudFrontKeyValueStoreClient: ...
@overload
def client(
    service_name: Literal["cloudhsm"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudHSMClient: ...
@overload
def client(
    service_name: Literal["cloudhsmv2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudHSMV2Client: ...
@overload
def client(
    service_name: Literal["cloudsearch"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudSearchClient: ...
@overload
def client(
    service_name: Literal["cloudsearchdomain"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudSearchDomainClient: ...
@overload
def client(
    service_name: Literal["cloudtrail"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudTrailClient: ...
@overload
def client(
    service_name: Literal["cloudtrail-data"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudTrailDataServiceClient: ...
@overload
def client(
    service_name: Literal["cloudwatch"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudWatchClient: ...
@overload
def client(
    service_name: Literal["codeartifact"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeArtifactClient: ...
@overload
def client(
    service_name: Literal["codebuild"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeBuildClient: ...
@overload
def client(
    service_name: Literal["codecatalyst"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeCatalystClient: ...
@overload
def client(
    service_name: Literal["codecommit"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeCommitClient: ...
@overload
def client(
    service_name: Literal["codeconnections"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeConnectionsClient: ...
@overload
def client(
    service_name: Literal["codedeploy"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeDeployClient: ...
@overload
def client(
    service_name: Literal["codeguru-reviewer"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeGuruReviewerClient: ...
@overload
def client(
    service_name: Literal["codeguru-security"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeGuruSecurityClient: ...
@overload
def client(
    service_name: Literal["codeguruprofiler"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeGuruProfilerClient: ...
@overload
def client(
    service_name: Literal["codepipeline"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodePipelineClient: ...
@overload
def client(
    service_name: Literal["codestar"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeStarClient: ...
@overload
def client(
    service_name: Literal["codestar-connections"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeStarconnectionsClient: ...
@overload
def client(
    service_name: Literal["codestar-notifications"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CodeStarNotificationsClient: ...
@overload
def client(
    service_name: Literal["cognito-identity"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CognitoIdentityClient: ...
@overload
def client(
    service_name: Literal["cognito-idp"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CognitoIdentityProviderClient: ...
@overload
def client(
    service_name: Literal["cognito-sync"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CognitoSyncClient: ...
@overload
def client(
    service_name: Literal["comprehend"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ComprehendClient: ...
@overload
def client(
    service_name: Literal["comprehendmedical"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ComprehendMedicalClient: ...
@overload
def client(
    service_name: Literal["compute-optimizer"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ComputeOptimizerClient: ...
@overload
def client(
    service_name: Literal["config"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ConfigServiceClient: ...
@overload
def client(
    service_name: Literal["connect"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ConnectClient: ...
@overload
def client(
    service_name: Literal["connect-contact-lens"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ConnectContactLensClient: ...
@overload
def client(
    service_name: Literal["connectcampaigns"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ConnectCampaignServiceClient: ...
@overload
def client(
    service_name: Literal["connectcases"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ConnectCasesClient: ...
@overload
def client(
    service_name: Literal["connectparticipant"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ConnectParticipantClient: ...
@overload
def client(
    service_name: Literal["controlcatalog"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ControlCatalogClient: ...
@overload
def client(
    service_name: Literal["controltower"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ControlTowerClient: ...
@overload
def client(
    service_name: Literal["cost-optimization-hub"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CostOptimizationHubClient: ...
@overload
def client(
    service_name: Literal["cur"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CostandUsageReportServiceClient: ...
@overload
def client(
    service_name: Literal["customer-profiles"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CustomerProfilesClient: ...
@overload
def client(
    service_name: Literal["databrew"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> GlueDataBrewClient: ...
@overload
def client(
    service_name: Literal["dataexchange"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DataExchangeClient: ...
@overload
def client(
    service_name: Literal["datapipeline"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DataPipelineClient: ...
@overload
def client(
    service_name: Literal["datasync"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DataSyncClient: ...
@overload
def client(
    service_name: Literal["datazone"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DataZoneClient: ...
@overload
def client(
    service_name: Literal["dax"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DAXClient: ...
@overload
def client(
    service_name: Literal["deadline"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DeadlineCloudClient: ...
@overload
def client(
    service_name: Literal["detective"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DetectiveClient: ...
@overload
def client(
    service_name: Literal["devicefarm"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DeviceFarmClient: ...
@overload
def client(
    service_name: Literal["devops-guru"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DevOpsGuruClient: ...
@overload
def client(
    service_name: Literal["directconnect"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DirectConnectClient: ...
@overload
def client(
    service_name: Literal["discovery"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ApplicationDiscoveryServiceClient: ...
@overload
def client(
    service_name: Literal["dlm"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DLMClient: ...
@overload
def client(
    service_name: Literal["dms"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DatabaseMigrationServiceClient: ...
@overload
def client(
    service_name: Literal["docdb"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DocDBClient: ...
@overload
def client(
    service_name: Literal["docdb-elastic"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DocDBElasticClient: ...
@overload
def client(
    service_name: Literal["drs"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DrsClient: ...
@overload
def client(
    service_name: Literal["ds"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DirectoryServiceClient: ...
@overload
def client(
    service_name: Literal["dynamodb"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DynamoDBClient: ...
@overload
def client(
    service_name: Literal["dynamodbstreams"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DynamoDBStreamsClient: ...
@overload
def client(
    service_name: Literal["ebs"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EBSClient: ...
@overload
def client(
    service_name: Literal["ec2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EC2Client: ...
@overload
def client(
    service_name: Literal["ec2-instance-connect"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EC2InstanceConnectClient: ...
@overload
def client(
    service_name: Literal["ecr"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ECRClient: ...
@overload
def client(
    service_name: Literal["ecr-public"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ECRPublicClient: ...
@overload
def client(
    service_name: Literal["ecs"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ECSClient: ...
@overload
def client(
    service_name: Literal["efs"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EFSClient: ...
@overload
def client(
    service_name: Literal["eks"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EKSClient: ...
@overload
def client(
    service_name: Literal["eks-auth"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EKSAuthClient: ...
@overload
def client(
    service_name: Literal["elastic-inference"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ElasticInferenceClient: ...
@overload
def client(
    service_name: Literal["elasticache"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ElastiCacheClient: ...
@overload
def client(
    service_name: Literal["elasticbeanstalk"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ElasticBeanstalkClient: ...
@overload
def client(
    service_name: Literal["elastictranscoder"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ElasticTranscoderClient: ...
@overload
def client(
    service_name: Literal["elb"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ElasticLoadBalancingClient: ...
@overload
def client(
    service_name: Literal["elbv2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ElasticLoadBalancingv2Client: ...
@overload
def client(
    service_name: Literal["emr"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EMRClient: ...
@overload
def client(
    service_name: Literal["emr-containers"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EMRContainersClient: ...
@overload
def client(
    service_name: Literal["emr-serverless"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EMRServerlessClient: ...
@overload
def client(
    service_name: Literal["entityresolution"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EntityResolutionClient: ...
@overload
def client(
    service_name: Literal["es"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ElasticsearchServiceClient: ...
@overload
def client(
    service_name: Literal["events"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EventBridgeClient: ...
@overload
def client(
    service_name: Literal["evidently"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudWatchEvidentlyClient: ...
@overload
def client(
    service_name: Literal["finspace"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> FinspaceClient: ...
@overload
def client(
    service_name: Literal["finspace-data"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> FinSpaceDataClient: ...
@overload
def client(
    service_name: Literal["firehose"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> FirehoseClient: ...
@overload
def client(
    service_name: Literal["fis"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> FISClient: ...
@overload
def client(
    service_name: Literal["fms"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> FMSClient: ...
@overload
def client(
    service_name: Literal["forecast"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ForecastServiceClient: ...
@overload
def client(
    service_name: Literal["forecastquery"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ForecastQueryServiceClient: ...
@overload
def client(
    service_name: Literal["frauddetector"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> FraudDetectorClient: ...
@overload
def client(
    service_name: Literal["freetier"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> FreeTierClient: ...
@overload
def client(
    service_name: Literal["fsx"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> FSxClient: ...
@overload
def client(
    service_name: Literal["gamelift"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> GameLiftClient: ...
@overload
def client(
    service_name: Literal["glacier"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> GlacierClient: ...
@overload
def client(
    service_name: Literal["globalaccelerator"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> GlobalAcceleratorClient: ...
@overload
def client(
    service_name: Literal["glue"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> GlueClient: ...
@overload
def client(
    service_name: Literal["grafana"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ManagedGrafanaClient: ...
@overload
def client(
    service_name: Literal["greengrass"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> GreengrassClient: ...
@overload
def client(
    service_name: Literal["greengrassv2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> GreengrassV2Client: ...
@overload
def client(
    service_name: Literal["groundstation"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> GroundStationClient: ...
@overload
def client(
    service_name: Literal["guardduty"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> GuardDutyClient: ...
@overload
def client(
    service_name: Literal["health"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> HealthClient: ...
@overload
def client(
    service_name: Literal["healthlake"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> HealthLakeClient: ...
@overload
def client(
    service_name: Literal["iam"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IAMClient: ...
@overload
def client(
    service_name: Literal["identitystore"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IdentityStoreClient: ...
@overload
def client(
    service_name: Literal["imagebuilder"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ImagebuilderClient: ...
@overload
def client(
    service_name: Literal["importexport"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ImportExportClient: ...
@overload
def client(
    service_name: Literal["inspector"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> InspectorClient: ...
@overload
def client(
    service_name: Literal["inspector-scan"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> InspectorscanClient: ...
@overload
def client(
    service_name: Literal["inspector2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Inspector2Client: ...
@overload
def client(
    service_name: Literal["internetmonitor"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudWatchInternetMonitorClient: ...
@overload
def client(
    service_name: Literal["iot"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTClient: ...
@overload
def client(
    service_name: Literal["iot-data"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTDataPlaneClient: ...
@overload
def client(
    service_name: Literal["iot-jobs-data"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTJobsDataPlaneClient: ...
@overload
def client(
    service_name: Literal["iot1click-devices"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoT1ClickDevicesServiceClient: ...
@overload
def client(
    service_name: Literal["iot1click-projects"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoT1ClickProjectsClient: ...
@overload
def client(
    service_name: Literal["iotanalytics"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTAnalyticsClient: ...
@overload
def client(
    service_name: Literal["iotdeviceadvisor"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTDeviceAdvisorClient: ...
@overload
def client(
    service_name: Literal["iotevents"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTEventsClient: ...
@overload
def client(
    service_name: Literal["iotevents-data"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTEventsDataClient: ...
@overload
def client(
    service_name: Literal["iotfleethub"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTFleetHubClient: ...
@overload
def client(
    service_name: Literal["iotfleetwise"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTFleetWiseClient: ...
@overload
def client(
    service_name: Literal["iotsecuretunneling"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTSecureTunnelingClient: ...
@overload
def client(
    service_name: Literal["iotsitewise"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTSiteWiseClient: ...
@overload
def client(
    service_name: Literal["iotthingsgraph"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTThingsGraphClient: ...
@overload
def client(
    service_name: Literal["iottwinmaker"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTTwinMakerClient: ...
@overload
def client(
    service_name: Literal["iotwireless"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IoTWirelessClient: ...
@overload
def client(
    service_name: Literal["ivs"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IVSClient: ...
@overload
def client(
    service_name: Literal["ivs-realtime"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IvsrealtimeClient: ...
@overload
def client(
    service_name: Literal["ivschat"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IvschatClient: ...
@overload
def client(
    service_name: Literal["kafka"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KafkaClient: ...
@overload
def client(
    service_name: Literal["kafkaconnect"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KafkaConnectClient: ...
@overload
def client(
    service_name: Literal["kendra"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KendraClient: ...
@overload
def client(
    service_name: Literal["kendra-ranking"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KendraRankingClient: ...
@overload
def client(
    service_name: Literal["keyspaces"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KeyspacesClient: ...
@overload
def client(
    service_name: Literal["kinesis"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KinesisClient: ...
@overload
def client(
    service_name: Literal["kinesis-video-archived-media"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KinesisVideoArchivedMediaClient: ...
@overload
def client(
    service_name: Literal["kinesis-video-media"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KinesisVideoMediaClient: ...
@overload
def client(
    service_name: Literal["kinesis-video-signaling"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KinesisVideoSignalingChannelsClient: ...
@overload
def client(
    service_name: Literal["kinesis-video-webrtc-storage"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KinesisVideoWebRTCStorageClient: ...
@overload
def client(
    service_name: Literal["kinesisanalytics"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KinesisAnalyticsClient: ...
@overload
def client(
    service_name: Literal["kinesisanalyticsv2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KinesisAnalyticsV2Client: ...
@overload
def client(
    service_name: Literal["kinesisvideo"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KinesisVideoClient: ...
@overload
def client(
    service_name: Literal["kms"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> KMSClient: ...
@overload
def client(
    service_name: Literal["lakeformation"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LakeFormationClient: ...
@overload
def client(
    service_name: Literal["lambda"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LambdaClient: ...
@overload
def client(
    service_name: Literal["launch-wizard"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LaunchWizardClient: ...
@overload
def client(
    service_name: Literal["lex-models"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LexModelBuildingServiceClient: ...
@overload
def client(
    service_name: Literal["lex-runtime"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LexRuntimeServiceClient: ...
@overload
def client(
    service_name: Literal["lexv2-models"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LexModelsV2Client: ...
@overload
def client(
    service_name: Literal["lexv2-runtime"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LexRuntimeV2Client: ...
@overload
def client(
    service_name: Literal["license-manager"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LicenseManagerClient: ...
@overload
def client(
    service_name: Literal["license-manager-linux-subscriptions"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LicenseManagerLinuxSubscriptionsClient: ...
@overload
def client(
    service_name: Literal["license-manager-user-subscriptions"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LicenseManagerUserSubscriptionsClient: ...
@overload
def client(
    service_name: Literal["lightsail"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LightsailClient: ...
@overload
def client(
    service_name: Literal["location"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LocationServiceClient: ...
@overload
def client(
    service_name: Literal["logs"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudWatchLogsClient: ...
@overload
def client(
    service_name: Literal["lookoutequipment"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LookoutEquipmentClient: ...
@overload
def client(
    service_name: Literal["lookoutmetrics"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LookoutMetricsClient: ...
@overload
def client(
    service_name: Literal["lookoutvision"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> LookoutforVisionClient: ...
@overload
def client(
    service_name: Literal["m2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MainframeModernizationClient: ...
@overload
def client(
    service_name: Literal["machinelearning"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MachineLearningClient: ...
@overload
def client(
    service_name: Literal["macie2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Macie2Client: ...
@overload
def client(
    service_name: Literal["mailmanager"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MailManagerClient: ...
@overload
def client(
    service_name: Literal["managedblockchain"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ManagedBlockchainClient: ...
@overload
def client(
    service_name: Literal["managedblockchain-query"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ManagedBlockchainQueryClient: ...
@overload
def client(
    service_name: Literal["marketplace-agreement"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AgreementServiceClient: ...
@overload
def client(
    service_name: Literal["marketplace-catalog"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MarketplaceCatalogClient: ...
@overload
def client(
    service_name: Literal["marketplace-deployment"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MarketplaceDeploymentServiceClient: ...
@overload
def client(
    service_name: Literal["marketplace-entitlement"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MarketplaceEntitlementServiceClient: ...
@overload
def client(
    service_name: Literal["marketplacecommerceanalytics"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MarketplaceCommerceAnalyticsClient: ...
@overload
def client(
    service_name: Literal["mediaconnect"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MediaConnectClient: ...
@overload
def client(
    service_name: Literal["mediaconvert"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MediaConvertClient: ...
@overload
def client(
    service_name: Literal["medialive"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MediaLiveClient: ...
@overload
def client(
    service_name: Literal["mediapackage"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MediaPackageClient: ...
@overload
def client(
    service_name: Literal["mediapackage-vod"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MediaPackageVodClient: ...
@overload
def client(
    service_name: Literal["mediapackagev2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Mediapackagev2Client: ...
@overload
def client(
    service_name: Literal["mediastore"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MediaStoreClient: ...
@overload
def client(
    service_name: Literal["mediastore-data"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MediaStoreDataClient: ...
@overload
def client(
    service_name: Literal["mediatailor"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MediaTailorClient: ...
@overload
def client(
    service_name: Literal["medical-imaging"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> HealthImagingClient: ...
@overload
def client(
    service_name: Literal["memorydb"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MemoryDBClient: ...
@overload
def client(
    service_name: Literal["meteringmarketplace"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MarketplaceMeteringClient: ...
@overload
def client(
    service_name: Literal["mgh"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MigrationHubClient: ...
@overload
def client(
    service_name: Literal["mgn"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MgnClient: ...
@overload
def client(
    service_name: Literal["migration-hub-refactor-spaces"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MigrationHubRefactorSpacesClient: ...
@overload
def client(
    service_name: Literal["migrationhub-config"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MigrationHubConfigClient: ...
@overload
def client(
    service_name: Literal["migrationhuborchestrator"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MigrationHubOrchestratorClient: ...
@overload
def client(
    service_name: Literal["migrationhubstrategy"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MigrationHubStrategyRecommendationsClient: ...
@overload
def client(
    service_name: Literal["mobile"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MobileClient: ...
@overload
def client(
    service_name: Literal["mq"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MQClient: ...
@overload
def client(
    service_name: Literal["mturk"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MTurkClient: ...
@overload
def client(
    service_name: Literal["mwaa"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> MWAAClient: ...
@overload
def client(
    service_name: Literal["neptune"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> NeptuneClient: ...
@overload
def client(
    service_name: Literal["neptune-graph"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> NeptuneGraphClient: ...
@overload
def client(
    service_name: Literal["neptunedata"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> NeptuneDataClient: ...
@overload
def client(
    service_name: Literal["network-firewall"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> NetworkFirewallClient: ...
@overload
def client(
    service_name: Literal["networkmanager"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> NetworkManagerClient: ...
@overload
def client(
    service_name: Literal["networkmonitor"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudWatchNetworkMonitorClient: ...
@overload
def client(
    service_name: Literal["nimble"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> NimbleStudioClient: ...
@overload
def client(
    service_name: Literal["oam"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudWatchObservabilityAccessManagerClient: ...
@overload
def client(
    service_name: Literal["omics"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> OmicsClient: ...
@overload
def client(
    service_name: Literal["opensearch"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> OpenSearchServiceClient: ...
@overload
def client(
    service_name: Literal["opensearchserverless"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> OpenSearchServiceServerlessClient: ...
@overload
def client(
    service_name: Literal["opsworks"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> OpsWorksClient: ...
@overload
def client(
    service_name: Literal["opsworkscm"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> OpsWorksCMClient: ...
@overload
def client(
    service_name: Literal["organizations"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> OrganizationsClient: ...
@overload
def client(
    service_name: Literal["osis"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> OpenSearchIngestionClient: ...
@overload
def client(
    service_name: Literal["outposts"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> OutpostsClient: ...
@overload
def client(
    service_name: Literal["panorama"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PanoramaClient: ...
@overload
def client(
    service_name: Literal["payment-cryptography"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PaymentCryptographyControlPlaneClient: ...
@overload
def client(
    service_name: Literal["payment-cryptography-data"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PaymentCryptographyDataPlaneClient: ...
@overload
def client(
    service_name: Literal["pca-connector-ad"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PcaConnectorAdClient: ...
@overload
def client(
    service_name: Literal["pca-connector-scep"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PrivateCAConnectorforSCEPClient: ...
@overload
def client(
    service_name: Literal["personalize"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PersonalizeClient: ...
@overload
def client(
    service_name: Literal["personalize-events"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PersonalizeEventsClient: ...
@overload
def client(
    service_name: Literal["personalize-runtime"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PersonalizeRuntimeClient: ...
@overload
def client(
    service_name: Literal["pi"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PIClient: ...
@overload
def client(
    service_name: Literal["pinpoint"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PinpointClient: ...
@overload
def client(
    service_name: Literal["pinpoint-email"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PinpointEmailClient: ...
@overload
def client(
    service_name: Literal["pinpoint-sms-voice"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PinpointSMSVoiceClient: ...
@overload
def client(
    service_name: Literal["pinpoint-sms-voice-v2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PinpointSMSVoiceV2Client: ...
@overload
def client(
    service_name: Literal["pipes"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EventBridgePipesClient: ...
@overload
def client(
    service_name: Literal["polly"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PollyClient: ...
@overload
def client(
    service_name: Literal["pricing"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PricingClient: ...
@overload
def client(
    service_name: Literal["privatenetworks"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Private5GClient: ...
@overload
def client(
    service_name: Literal["proton"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ProtonClient: ...
@overload
def client(
    service_name: Literal["qbusiness"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> QBusinessClient: ...
@overload
def client(
    service_name: Literal["qconnect"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> QConnectClient: ...
@overload
def client(
    service_name: Literal["qldb"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> QLDBClient: ...
@overload
def client(
    service_name: Literal["qldb-session"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> QLDBSessionClient: ...
@overload
def client(
    service_name: Literal["quicksight"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> QuickSightClient: ...
@overload
def client(
    service_name: Literal["ram"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> RAMClient: ...
@overload
def client(
    service_name: Literal["rbin"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> RecycleBinClient: ...
@overload
def client(
    service_name: Literal["rds"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> RDSClient: ...
@overload
def client(
    service_name: Literal["rds-data"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> RDSDataServiceClient: ...
@overload
def client(
    service_name: Literal["redshift"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> RedshiftClient: ...
@overload
def client(
    service_name: Literal["redshift-data"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> RedshiftDataAPIServiceClient: ...
@overload
def client(
    service_name: Literal["redshift-serverless"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> RedshiftServerlessClient: ...
@overload
def client(
    service_name: Literal["rekognition"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> RekognitionClient: ...
@overload
def client(
    service_name: Literal["repostspace"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> RePostPrivateClient: ...
@overload
def client(
    service_name: Literal["resiliencehub"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ResilienceHubClient: ...
@overload
def client(
    service_name: Literal["resource-explorer-2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ResourceExplorerClient: ...
@overload
def client(
    service_name: Literal["resource-groups"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ResourceGroupsClient: ...
@overload
def client(
    service_name: Literal["resourcegroupstaggingapi"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ResourceGroupsTaggingAPIClient: ...
@overload
def client(
    service_name: Literal["robomaker"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> RoboMakerClient: ...
@overload
def client(
    service_name: Literal["rolesanywhere"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IAMRolesAnywhereClient: ...
@overload
def client(
    service_name: Literal["route53"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Route53Client: ...
@overload
def client(
    service_name: Literal["route53-recovery-cluster"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Route53RecoveryClusterClient: ...
@overload
def client(
    service_name: Literal["route53-recovery-control-config"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Route53RecoveryControlConfigClient: ...
@overload
def client(
    service_name: Literal["route53-recovery-readiness"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Route53RecoveryReadinessClient: ...
@overload
def client(
    service_name: Literal["route53domains"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Route53DomainsClient: ...
@overload
def client(
    service_name: Literal["route53profiles"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Route53ProfilesClient: ...
@overload
def client(
    service_name: Literal["route53resolver"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> Route53ResolverClient: ...
@overload
def client(
    service_name: Literal["rum"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudWatchRUMClient: ...
@overload
def client(
    service_name: Literal["s3"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> S3Client: ...
@overload
def client(
    service_name: Literal["s3control"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> S3ControlClient: ...
@overload
def client(
    service_name: Literal["s3outposts"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> S3OutpostsClient: ...
@overload
def client(
    service_name: Literal["sagemaker"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SageMakerClient: ...
@overload
def client(
    service_name: Literal["sagemaker-a2i-runtime"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AugmentedAIRuntimeClient: ...
@overload
def client(
    service_name: Literal["sagemaker-edge"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SagemakerEdgeManagerClient: ...
@overload
def client(
    service_name: Literal["sagemaker-featurestore-runtime"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SageMakerFeatureStoreRuntimeClient: ...
@overload
def client(
    service_name: Literal["sagemaker-geospatial"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SageMakergeospatialcapabilitiesClient: ...
@overload
def client(
    service_name: Literal["sagemaker-metrics"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SageMakerMetricsClient: ...
@overload
def client(
    service_name: Literal["sagemaker-runtime"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SageMakerRuntimeClient: ...
@overload
def client(
    service_name: Literal["savingsplans"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SavingsPlansClient: ...
@overload
def client(
    service_name: Literal["scheduler"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EventBridgeSchedulerClient: ...
@overload
def client(
    service_name: Literal["schemas"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SchemasClient: ...
@overload
def client(
    service_name: Literal["sdb"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SimpleDBClient: ...
@overload
def client(
    service_name: Literal["secretsmanager"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SecretsManagerClient: ...
@overload
def client(
    service_name: Literal["securityhub"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SecurityHubClient: ...
@overload
def client(
    service_name: Literal["securitylake"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SecurityLakeClient: ...
@overload
def client(
    service_name: Literal["serverlessrepo"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ServerlessApplicationRepositoryClient: ...
@overload
def client(
    service_name: Literal["service-quotas"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ServiceQuotasClient: ...
@overload
def client(
    service_name: Literal["servicecatalog"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ServiceCatalogClient: ...
@overload
def client(
    service_name: Literal["servicecatalog-appregistry"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> AppRegistryClient: ...
@overload
def client(
    service_name: Literal["servicediscovery"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ServiceDiscoveryClient: ...
@overload
def client(
    service_name: Literal["ses"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SESClient: ...
@overload
def client(
    service_name: Literal["sesv2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SESV2Client: ...
@overload
def client(
    service_name: Literal["shield"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ShieldClient: ...
@overload
def client(
    service_name: Literal["signer"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SignerClient: ...
@overload
def client(
    service_name: Literal["simspaceweaver"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SimSpaceWeaverClient: ...
@overload
def client(
    service_name: Literal["sms"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SMSClient: ...
@overload
def client(
    service_name: Literal["sms-voice"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> PinpointSMSVoiceClient: ...
@overload
def client(
    service_name: Literal["snow-device-management"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SnowDeviceManagementClient: ...
@overload
def client(
    service_name: Literal["snowball"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SnowballClient: ...
@overload
def client(
    service_name: Literal["sns"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SNSClient: ...
@overload
def client(
    service_name: Literal["sqs"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SQSClient: ...
@overload
def client(
    service_name: Literal["ssm"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SSMClient: ...
@overload
def client(
    service_name: Literal["ssm-contacts"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SSMContactsClient: ...
@overload
def client(
    service_name: Literal["ssm-incidents"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SSMIncidentsClient: ...
@overload
def client(
    service_name: Literal["ssm-sap"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SsmSapClient: ...
@overload
def client(
    service_name: Literal["sso"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SSOClient: ...
@overload
def client(
    service_name: Literal["sso-admin"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SSOAdminClient: ...
@overload
def client(
    service_name: Literal["sso-oidc"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SSOOIDCClient: ...
@overload
def client(
    service_name: Literal["stepfunctions"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SFNClient: ...
@overload
def client(
    service_name: Literal["storagegateway"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> StorageGatewayClient: ...
@overload
def client(
    service_name: Literal["sts"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> STSClient: ...
@overload
def client(
    service_name: Literal["supplychain"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SupplyChainClient: ...
@overload
def client(
    service_name: Literal["support"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SupportClient: ...
@overload
def client(
    service_name: Literal["support-app"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SupportAppClient: ...
@overload
def client(
    service_name: Literal["swf"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SWFClient: ...
@overload
def client(
    service_name: Literal["synthetics"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SyntheticsClient: ...
@overload
def client(
    service_name: Literal["taxsettings"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> TaxSettingsClient: ...
@overload
def client(
    service_name: Literal["textract"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> TextractClient: ...
@overload
def client(
    service_name: Literal["timestream-influxdb"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> TimestreamInfluxDBClient: ...
@overload
def client(
    service_name: Literal["timestream-query"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> TimestreamQueryClient: ...
@overload
def client(
    service_name: Literal["timestream-write"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> TimestreamWriteClient: ...
@overload
def client(
    service_name: Literal["tnb"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> TelcoNetworkBuilderClient: ...
@overload
def client(
    service_name: Literal["transcribe"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> TranscribeServiceClient: ...
@overload
def client(
    service_name: Literal["transfer"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> TransferClient: ...
@overload
def client(
    service_name: Literal["translate"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> TranslateClient: ...
@overload
def client(
    service_name: Literal["trustedadvisor"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> TrustedAdvisorPublicAPIClient: ...
@overload
def client(
    service_name: Literal["verifiedpermissions"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> VerifiedPermissionsClient: ...
@overload
def client(
    service_name: Literal["voice-id"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> VoiceIDClient: ...
@overload
def client(
    service_name: Literal["vpc-lattice"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> VPCLatticeClient: ...
@overload
def client(
    service_name: Literal["waf"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WAFClient: ...
@overload
def client(
    service_name: Literal["waf-regional"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WAFRegionalClient: ...
@overload
def client(
    service_name: Literal["wafv2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WAFV2Client: ...
@overload
def client(
    service_name: Literal["wellarchitected"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WellArchitectedClient: ...
@overload
def client(
    service_name: Literal["wisdom"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> ConnectWisdomServiceClient: ...
@overload
def client(
    service_name: Literal["workdocs"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WorkDocsClient: ...
@overload
def client(
    service_name: Literal["worklink"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WorkLinkClient: ...
@overload
def client(
    service_name: Literal["workmail"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WorkMailClient: ...
@overload
def client(
    service_name: Literal["workmailmessageflow"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WorkMailMessageFlowClient: ...
@overload
def client(
    service_name: Literal["workspaces"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WorkSpacesClient: ...
@overload
def client(
    service_name: Literal["workspaces-thin-client"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WorkSpacesThinClientClient: ...
@overload
def client(
    service_name: Literal["workspaces-web"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> WorkSpacesWebClient: ...
@overload
def client(
    service_name: Literal["xray"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> XRayClient: ...
@overload
def resource(
    service_name: Literal["cloudformation"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudFormationServiceResource: ...
@overload
def resource(
    service_name: Literal["cloudwatch"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> CloudWatchServiceResource: ...
@overload
def resource(
    service_name: Literal["dynamodb"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> DynamoDBServiceResource: ...
@overload
def resource(
    service_name: Literal["ec2"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> EC2ServiceResource: ...
@overload
def resource(
    service_name: Literal["glacier"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> GlacierServiceResource: ...
@overload
def resource(
    service_name: Literal["iam"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> IAMServiceResource: ...
@overload
def resource(
    service_name: Literal["opsworks"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> OpsWorksServiceResource: ...
@overload
def resource(
    service_name: Literal["s3"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> S3ServiceResource: ...
@overload
def resource(
    service_name: Literal["sns"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SNSServiceResource: ...
@overload
def resource(
    service_name: Literal["sqs"],
    region_name: Optional[str] = ...,
    api_version: Optional[str] = ...,
    use_ssl: Optional[bool] = ...,
    verify: Union[bool, str, None] = ...,
    endpoint_url: Optional[str] = ...,
    aws_access_key_id: Optional[str] = ...,
    aws_secret_access_key: Optional[str] = ...,
    aws_session_token: Optional[str] = ...,
    config: Optional[Config] = ...,
) -> SQSServiceResource: ...
