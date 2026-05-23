from app.core.neurosploit.vuln_engine.testers.base_tester import BaseTester
from app.core.neurosploit.vuln_engine.testers.injection import (
    XSSReflectedTester, XSSStoredTester, XSSDomTester,
    SQLiErrorTester, SQLiUnionTester, SQLiBlindTester, SQLiTimeTester,
    CommandInjectionTester, SSTITester, NoSQLInjectionTester,
)
from app.core.neurosploit.vuln_engine.testers.auth import (
    AuthBypassTester, JWTManipulationTester, SessionFixationTester,
    WeakPasswordTester, DefaultCredentialsTester, TwoFactorBypassTester,
    OauthMisconfigTester,
)
from app.core.neurosploit.vuln_engine.testers.authorization import (
    IDORTester, BOLATester, PrivilegeEscalationTester,
    BflaTester, MassAssignmentTester, ForcedBrowsingTester,
)
from app.core.neurosploit.vuln_engine.testers.file_access import (
    LFITester, RFITester, PathTraversalTester, XXETester, FileUploadTester,
    ArbitraryFileReadTester, ArbitraryFileDeleteTester, ZipSlipTester,
)
from app.core.neurosploit.vuln_engine.testers.request_forgery import (
    SSRFTester, CSRFTester, GraphqlIntrospectionTester, GraphqlDosTester,
)
from app.core.neurosploit.vuln_engine.testers.client_side import (
    CORSTester, ClickjackingTester, OpenRedirectTester,
    DomClobberingTester, PostMessageVulnTester, WebsocketHijackTester,
    PrototypePollutionTester, CssInjectionTester, TabnabbingTester,
)
from app.core.neurosploit.vuln_engine.testers.infrastructure import (
    SecurityHeadersTester, SSLTester, HTTPMethodsTester,
    DirectoryListingTester, DebugModeTester, ExposedAdminPanelTester,
    ExposedApiDocsTester, InsecureCookieFlagsTester,
)
from app.core.neurosploit.vuln_engine.testers.data_exposure import (
    SensitiveDataExposureTester, InformationDisclosureTester,
    ApiKeyExposureTester, SourceCodeDisclosureTester,
    BackupFileExposureTester, VersionDisclosureTester,
)
from app.core.neurosploit.vuln_engine.testers.cloud_supply import (
    S3BucketMisconfigTester, CloudMetadataExposureTester,
    SubdomainTakeoverTester, VulnerableDependencyTester,
    ContainerEscapeTester, ServerlessMisconfigTester,
)
from app.core.neurosploit.vuln_engine.testers.advanced_injection import (
    LdapInjectionTester, XpathInjectionTester, GraphqlInjectionTester,
    CrlfInjectionTester, HeaderInjectionTester, EmailInjectionTester,
    ELInjectionTester, LogInjectionTester, HtmlInjectionTester,
    CsvInjectionTester, OrmInjectionTester,
)
from app.core.neurosploit.vuln_engine.testers.logic import (
    RaceConditionTester, BusinessLogicTester, RateLimitBypassTester,
    ParameterPollutionTester, TypeJugglingTester, TimingAttackTester,
    HostHeaderInjectionTester,
)

ALL_TESTERS = [
    XSSReflectedTester, XSSStoredTester, XSSDomTester,
    SQLiErrorTester, SQLiUnionTester, SQLiBlindTester, SQLiTimeTester,
    CommandInjectionTester, SSTITester, NoSQLInjectionTester,
    LdapInjectionTester, XpathInjectionTester, GraphqlInjectionTester,
    CrlfInjectionTester, HeaderInjectionTester, EmailInjectionTester,
    ELInjectionTester, LogInjectionTester, HtmlInjectionTester,
    CsvInjectionTester, OrmInjectionTester,
    AuthBypassTester, JWTManipulationTester, SessionFixationTester,
    WeakPasswordTester, DefaultCredentialsTester, TwoFactorBypassTester,
    OauthMisconfigTester,
    IDORTester, BOLATester, PrivilegeEscalationTester,
    BflaTester, MassAssignmentTester, ForcedBrowsingTester,
    LFITester, RFITester, PathTraversalTester, XXETester, FileUploadTester,
    ArbitraryFileReadTester, ArbitraryFileDeleteTester, ZipSlipTester,
    SSRFTester, CSRFTester, GraphqlIntrospectionTester, GraphqlDosTester,
    CORSTester, ClickjackingTester, OpenRedirectTester,
    DomClobberingTester, PostMessageVulnTester, WebsocketHijackTester,
    PrototypePollutionTester, CssInjectionTester, TabnabbingTester,
    SecurityHeadersTester, SSLTester, HTTPMethodsTester,
    DirectoryListingTester, DebugModeTester, ExposedAdminPanelTester,
    ExposedApiDocsTester, InsecureCookieFlagsTester,
    SensitiveDataExposureTester, InformationDisclosureTester,
    ApiKeyExposureTester, SourceCodeDisclosureTester,
    BackupFileExposureTester, VersionDisclosureTester,
    S3BucketMisconfigTester, CloudMetadataExposureTester,
    SubdomainTakeoverTester, VulnerableDependencyTester,
    ContainerEscapeTester, ServerlessMisconfigTester,
    RaceConditionTester, BusinessLogicTester, RateLimitBypassTester,
    ParameterPollutionTester, TypeJugglingTester, TimingAttackTester,
    HostHeaderInjectionTester,
]
