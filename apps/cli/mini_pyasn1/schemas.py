# The ASN.1 modules mini_pyasn1 runs, written as data: mk.py dumps DEFS
# to data/schemas.json, and oracle.py and mini_pyasn1.kara both build
# pyasn1 types from it.
#
# A definition is {"def": name, "class": base, ...} and becomes
#     class name(base): <class attributes>
# like the classes in pyasn1-modules. A type expression is a type name,
# or {"t": name, ...} with any of
#     "of": type        componentType of a SEQUENCE OF / SET OF
#     "fields": [...]   componentType of a SEQUENCE / SET / CHOICE
#     "impl"/"expl": [class, id]   .subtype(implicitTag/explicitTag)
#     "sub": [cons]     .subtype(subtypeSpec=...)
#     "size": [cons]    .subtype(sizeSpec=...)
#     "named": [[n,v]]  .subtype(namedValues=...)
#     "value": v        .clone(v)
# A field is {"n": name, "t": type} plus "opt": true, "default": true
# (the type then carries the default "value"), or "open": [governing
# field, [[oid, type], ...]].
# Constraints: {"range": [lo, hi]}, {"size": [lo, hi]}, {"single": [...]},
# {"alpha": "chars"}, {"union": [...]}, {"inter": [...]}, {"excl": c};
# "MAX" is float('inf') as pyasn1-modules spells it.

DEFS = [
    # RFC 5280: the parts of an X.509 certificate.
    {"def": "Version", "class": "Integer", "named": [["v1", 0], ["v2", 1], ["v3", 2]]},
    {"def": "CertificateSerialNumber", "class": "Integer"},
    {"def": "UniqueIdentifier", "class": "BitString"},
    {"def": "AttributeType", "class": "ObjectIdentifier"},
    {"def": "AttributeValue", "class": "Any"},
    {"def": "DirectoryString", "class": "Choice", "fields": [
        {"n": "teletexString", "t": {"t": "TeletexString", "sub": [{"size": [1, "MAX"]}]}},
        {"n": "printableString", "t": {"t": "PrintableString", "sub": [{"size": [1, "MAX"]}]}},
        {"n": "universalString", "t": {"t": "UniversalString", "sub": [{"size": [1, "MAX"]}]}},
        {"n": "utf8String", "t": {"t": "UTF8String", "sub": [{"size": [1, "MAX"]}]}},
        {"n": "bmpString", "t": {"t": "BMPString", "sub": [{"size": [1, "MAX"]}]}},
    ]},
    {"def": "X520countryName", "class": "PrintableString", "cons": [{"size": [2, 2]}]},
    {"def": "EmailAddress", "class": "IA5String", "cons": [{"size": [1, 255]}]},
    {"def": "DomainComponent", "class": "IA5String"},
    {"def": "AttributeTypeAndValue", "class": "Sequence", "fields": [
        {"n": "type", "t": "AttributeType"},
        {"n": "value", "t": "AttributeValue", "open": ["type", [
            ["2.5.4.3", "DirectoryString"], ["2.5.4.4", "DirectoryString"],
            ["2.5.4.5", "PrintableString"], ["2.5.4.6", "X520countryName"],
            ["2.5.4.7", "DirectoryString"], ["2.5.4.8", "DirectoryString"],
            ["2.5.4.10", "DirectoryString"], ["2.5.4.11", "DirectoryString"],
            ["2.5.4.12", "DirectoryString"], ["2.5.4.42", "DirectoryString"],
            ["2.5.4.97", "DirectoryString"],
            ["1.2.840.113549.1.9.1", "EmailAddress"],
            ["0.9.2342.19200300.100.1.25", "DomainComponent"],
        ]]},
    ]},
    {"def": "RelativeDistinguishedName", "class": "SetOf", "of": "AttributeTypeAndValue",
     "cons": [{"size": [1, "MAX"]}]},
    {"def": "RDNSequence", "class": "SequenceOf", "of": "RelativeDistinguishedName"},
    {"def": "Name", "class": "Choice", "fields": [{"n": "rdnSequence", "t": "RDNSequence"}]},
    {"def": "Time", "class": "Choice", "fields": [
        {"n": "utcTime", "t": "UTCTime"}, {"n": "generalTime", "t": "GeneralizedTime"}]},
    {"def": "Validity", "class": "Sequence", "fields": [
        {"n": "notBefore", "t": "Time"}, {"n": "notAfter", "t": "Time"}]},
    {"def": "ECParameters", "class": "Choice", "fields": [{"n": "namedCurve", "t": "ObjectIdentifier"}]},
    {"def": "AlgorithmIdentifier", "class": "Sequence", "fields": [
        {"n": "algorithm", "t": "ObjectIdentifier"},
        {"n": "parameters", "t": "Any", "opt": True, "open": ["algorithm", [
            ["1.2.840.113549.1.1.1", "Null"], ["1.2.840.113549.1.1.5", "Null"],
            ["1.2.840.113549.1.1.11", "Null"], ["1.2.840.113549.1.1.12", "Null"],
            ["1.2.840.113549.1.1.13", "Null"], ["1.2.840.10045.2.1", "ECParameters"],
        ]]},
    ]},
    {"def": "SubjectPublicKeyInfo", "class": "Sequence", "fields": [
        {"n": "algorithm", "t": "AlgorithmIdentifier"}, {"n": "subjectPublicKey", "t": "BitString"}]},
    {"def": "Extension", "class": "Sequence", "fields": [
        {"n": "extnID", "t": "ObjectIdentifier"},
        {"n": "critical", "t": {"t": "Boolean", "value": False}, "default": True},
        {"n": "extnValue", "t": "OctetString"}]},
    {"def": "Extensions", "class": "SequenceOf", "of": "Extension", "cons": [{"size": [1, "MAX"]}]},
    {"def": "TBSCertificate", "class": "Sequence", "fields": [
        {"n": "version", "t": {"t": "Version", "expl": ["context", 0], "value": "v1"}, "default": True},
        {"n": "serialNumber", "t": "CertificateSerialNumber"},
        {"n": "signature", "t": "AlgorithmIdentifier"},
        {"n": "issuer", "t": "Name"},
        {"n": "validity", "t": "Validity"},
        {"n": "subject", "t": "Name"},
        {"n": "subjectPublicKeyInfo", "t": "SubjectPublicKeyInfo"},
        {"n": "issuerUniqueID", "t": {"t": "UniqueIdentifier", "impl": ["context", 1]}, "opt": True},
        {"n": "subjectUniqueID", "t": {"t": "UniqueIdentifier", "impl": ["context", 2]}, "opt": True},
        {"n": "extensions", "t": {"t": "Extensions", "expl": ["context", 3]}, "opt": True}]},
    {"def": "Certificate", "class": "Sequence", "fields": [
        {"n": "tbsCertificate", "t": "TBSCertificate"},
        {"n": "signatureAlgorithm", "t": "AlgorithmIdentifier"},
        {"n": "signature", "t": "BitString"}]},
    # The extensions mini_pyasn1's certificate tools look inside.
    {"def": "BasicConstraints", "class": "Sequence", "fields": [
        {"n": "cA", "t": {"t": "Boolean", "value": False}, "default": True},
        {"n": "pathLenConstraint", "t": {"t": "Integer", "sub": [{"range": [0, "MAX"]}]}, "opt": True}]},
    {"def": "KeyUsage", "class": "BitString", "named": [
        ["digitalSignature", 0], ["nonRepudiation", 1], ["keyEncipherment", 2],
        ["dataEncipherment", 3], ["keyAgreement", 4], ["keyCertSign", 5],
        ["cRLSign", 6], ["encipherOnly", 7], ["decipherOnly", 8]]},
    {"def": "KeyIdentifier", "class": "OctetString"},
    {"def": "SubjectKeyIdentifier", "class": "KeyIdentifier"},
    {"def": "AnotherName", "class": "Sequence", "fields": [
        {"n": "type-id", "t": "ObjectIdentifier"},
        {"n": "value", "t": {"t": "Any", "expl": ["context", 0]}}]},
    {"def": "GeneralName", "class": "Choice", "fields": [
        {"n": "otherName", "t": {"t": "AnotherName", "impl": ["context", 0]}},
        {"n": "rfc822Name", "t": {"t": "IA5String", "impl": ["context", 1]}},
        {"n": "dNSName", "t": {"t": "IA5String", "impl": ["context", 2]}},
        {"n": "directoryName", "t": {"t": "Name", "expl": ["context", 4]}},
        {"n": "uniformResourceIdentifier", "t": {"t": "IA5String", "impl": ["context", 6]}},
        {"n": "iPAddress", "t": {"t": "OctetString", "impl": ["context", 7]}},
        {"n": "registeredID", "t": {"t": "ObjectIdentifier", "impl": ["context", 8]}}]},
    {"def": "GeneralNames", "class": "SequenceOf", "of": "GeneralName", "cons": [{"size": [1, "MAX"]}]},
    {"def": "AuthorityKeyIdentifier", "class": "Sequence", "fields": [
        {"n": "keyIdentifier", "t": {"t": "KeyIdentifier", "impl": ["context", 0]}, "opt": True},
        {"n": "authorityCertIssuer", "t": {"t": "GeneralNames", "impl": ["context", 1]}, "opt": True},
        {"n": "authorityCertSerialNumber", "t": {"t": "CertificateSerialNumber", "impl": ["context", 2]}, "opt": True}]},
    {"def": "KeyPurposeId", "class": "ObjectIdentifier"},
    {"def": "ExtKeyUsageSyntax", "class": "SequenceOf", "of": "KeyPurposeId", "sizeSpec": [{"size": [1, "MAX"]}]},
    {"def": "PolicyQualifierInfo", "class": "Sequence", "fields": [
        {"n": "policyQualifierId", "t": "ObjectIdentifier"}, {"n": "qualifier", "t": "Any"}]},
    {"def": "PolicyInformation", "class": "Sequence", "fields": [
        {"n": "policyIdentifier", "t": "ObjectIdentifier"},
        {"n": "policyQualifiers", "t": {"t": "SequenceOf", "of": "PolicyQualifierInfo", "size": [{"size": [1, "MAX"]}]}, "opt": True}]},
    {"def": "CertificatePolicies", "class": "SequenceOf", "of": "PolicyInformation", "sizeSpec": [{"size": [1, "MAX"]}]},
    {"def": "DistributionPointName", "class": "Choice", "fields": [
        {"n": "fullName", "t": {"t": "GeneralNames", "impl": ["context", 0]}},
        {"n": "nameRelativeToCRLIssuer", "t": {"t": "RelativeDistinguishedName", "impl": ["context", 1]}}]},
    {"def": "ReasonFlags", "class": "BitString", "named": [
        ["unused", 0], ["keyCompromise", 1], ["cACompromise", 2], ["affiliationChanged", 3],
        ["superseded", 4], ["cessationOfOperation", 5], ["certificateHold", 6],
        ["privilegeWithdrawn", 7], ["aACompromise", 8]]},
    {"def": "DistributionPoint", "class": "Sequence", "fields": [
        {"n": "distributionPoint", "t": {"t": "DistributionPointName", "expl": ["context", 0]}, "opt": True},
        {"n": "reasons", "t": {"t": "ReasonFlags", "impl": ["context", 1]}, "opt": True},
        {"n": "cRLIssuer", "t": {"t": "GeneralNames", "impl": ["context", 2]}, "opt": True}]},
    {"def": "CRLDistributionPoints", "class": "SequenceOf", "of": "DistributionPoint", "sizeSpec": [{"size": [1, "MAX"]}]},
    {"def": "AccessDescription", "class": "Sequence", "fields": [
        {"n": "accessMethod", "t": "ObjectIdentifier"}, {"n": "accessLocation", "t": "GeneralName"}]},
    {"def": "AuthorityInfoAccessSyntax", "class": "SequenceOf", "of": "AccessDescription", "sizeSpec": [{"size": [1, "MAX"]}]},
    {"def": "PrivateKeyUsagePeriod", "class": "Sequence", "fields": [
        {"n": "notBefore", "t": {"t": "GeneralizedTime", "impl": ["context", 0]}, "opt": True},
        {"n": "notAfter", "t": {"t": "GeneralizedTime", "impl": ["context", 1]}, "opt": True}]},
    # RFC 8017 and RFC 5480: what the public key bit strings hold.
    {"def": "RSAPublicKey", "class": "Sequence", "fields": [
        {"n": "modulus", "t": "Integer"}, {"n": "publicExponent", "t": "Integer"}]},
    {"def": "ECDSA-Sig-Value", "class": "Sequence", "fields": [
        {"n": "r", "t": "Integer"}, {"n": "s", "t": "Integer"}]},
    # RFC 2986: a certificate signing request.
    {"def": "Attribute", "class": "Sequence", "fields": [
        {"n": "type", "t": "AttributeType"},
        {"n": "values", "t": {"t": "SetOf", "of": "AttributeValue"}}]},
    {"def": "CertificationRequestInfo", "class": "Sequence", "fields": [
        {"n": "version", "t": {"t": "Integer", "named": [["v1", 0]]}},
        {"n": "subject", "t": "Name"},
        {"n": "subjectPKInfo", "t": "SubjectPublicKeyInfo"},
        {"n": "attributes", "t": {"t": "SetOf", "of": "Attribute", "impl": ["context", 0]}}]},
    {"def": "CertificationRequest", "class": "Sequence", "fields": [
        {"n": "certificationRequestInfo", "t": "CertificationRequestInfo"},
        {"n": "signatureAlgorithm", "t": "AlgorithmIdentifier"},
        {"n": "signature", "t": "BitString"}]},
    # RFC 1902 / 1905 / 1901: SNMPv2c, as pysnmp's proto modules define it.
    {"def": "Integer32", "class": "Integer", "cons": [{"range": [-2147483648, 2147483647]}]},
    {"def": "IpAddress", "class": "OctetString", "tag": {"impl": ["application", 0]}, "cons": [{"size": [4, 4]}]},
    {"def": "Counter32", "class": "Integer", "tag": {"impl": ["application", 1]}, "cons": [{"range": [0, 4294967295]}]},
    {"def": "Gauge32", "class": "Integer", "tag": {"impl": ["application", 2]}, "cons": [{"range": [0, 4294967295]}]},
    {"def": "TimeTicks", "class": "Integer", "tag": {"impl": ["application", 3]}, "cons": [{"range": [0, 4294967295]}]},
    {"def": "Opaque", "class": "OctetString", "tag": {"impl": ["application", 4]}},
    {"def": "Counter64", "class": "Integer", "tag": {"impl": ["application", 6]}, "cons": [{"range": [0, 18446744073709551615]}]},
    {"def": "SimpleSyntax", "class": "Choice", "fields": [
        {"n": "integer-value", "t": "Integer32"},
        {"n": "string-value", "t": {"t": "OctetString", "sub": [{"size": [0, 65535]}]}},
        {"n": "objectID-value", "t": "ObjectIdentifier"}]},
    {"def": "ApplicationSyntax", "class": "Choice", "fields": [
        {"n": "ipAddress-value", "t": "IpAddress"}, {"n": "counter-value", "t": "Counter32"},
        {"n": "timeticks-value", "t": "TimeTicks"}, {"n": "arbitrary-value", "t": "Opaque"},
        {"n": "big-counter-value", "t": "Counter64"}, {"n": "gauge32-value", "t": "Gauge32"}]},
    {"def": "ObjectSyntax", "class": "Choice", "fields": [
        {"n": "simple", "t": "SimpleSyntax"}, {"n": "application-wide", "t": "ApplicationSyntax"}]},
    {"def": "BindValue", "class": "Choice", "fields": [
        {"n": "value", "t": "ObjectSyntax"},
        {"n": "unSpecified", "t": "Null"},
        {"n": "noSuchObject", "t": {"t": "Null", "impl": ["context", 0]}},
        {"n": "noSuchInstance", "t": {"t": "Null", "impl": ["context", 1]}},
        {"n": "endOfMibView", "t": {"t": "Null", "impl": ["context", 2]}}]},
    {"def": "VarBind", "class": "Sequence", "fields": [
        {"n": "name", "t": "ObjectIdentifier"}, {"n": "", "t": "BindValue"}]},
    {"def": "VarBindList", "class": "SequenceOf", "of": "VarBind", "cons": [{"size": [0, 2147483647]}]},
    {"def": "PDU", "class": "Sequence", "fields": [
        {"n": "request-id", "t": "Integer32"},
        {"n": "error-status", "t": {"t": "Integer", "named": [
            ["noError", 0], ["tooBig", 1], ["noSuchName", 2], ["badValue", 3], ["readOnly", 4],
            ["genErr", 5], ["noAccess", 6], ["wrongType", 7], ["wrongLength", 8],
            ["wrongEncoding", 9], ["wrongValue", 10], ["noCreation", 11], ["inconsistentValue", 12],
            ["resourceUnavailable", 13], ["commitFailed", 14], ["undoFailed", 15],
            ["authorizationError", 16], ["notWritable", 17], ["inconsistentName", 18]]}},
        {"n": "error-index", "t": {"t": "Integer", "sub": [{"range": [0, 2147483647]}]}},
        {"n": "variable-bindings", "t": "VarBindList"}]},
    {"def": "BulkPDU", "class": "Sequence", "fields": [
        {"n": "request-id", "t": "Integer32"},
        {"n": "non-repeaters", "t": {"t": "Integer", "sub": [{"range": [0, 2147483647]}]}},
        {"n": "max-repetitions", "t": {"t": "Integer", "sub": [{"range": [0, 2147483647]}]}},
        {"n": "variable-bindings", "t": "VarBindList"}]},
    {"def": "GetRequestPDU", "class": "PDU", "tag": {"impl": ["context", 0]}},
    {"def": "GetNextRequestPDU", "class": "PDU", "tag": {"impl": ["context", 1]}},
    {"def": "ResponsePDU", "class": "PDU", "tag": {"impl": ["context", 2]}},
    {"def": "SetRequestPDU", "class": "PDU", "tag": {"impl": ["context", 3]}},
    {"def": "GetBulkRequestPDU", "class": "BulkPDU", "tag": {"impl": ["context", 5]}},
    {"def": "InformRequestPDU", "class": "PDU", "tag": {"impl": ["context", 6]}},
    {"def": "SNMPv2TrapPDU", "class": "PDU", "tag": {"impl": ["context", 7]}},
    {"def": "ReportPDU", "class": "PDU", "tag": {"impl": ["context", 8]}},
    {"def": "PDUs", "class": "Choice", "fields": [
        {"n": "get-request", "t": "GetRequestPDU"}, {"n": "get-next-request", "t": "GetNextRequestPDU"},
        {"n": "get-bulk-request", "t": "GetBulkRequestPDU"}, {"n": "response", "t": "ResponsePDU"},
        {"n": "set-request", "t": "SetRequestPDU"}, {"n": "inform-request", "t": "InformRequestPDU"},
        {"n": "snmpV2-trap", "t": "SNMPv2TrapPDU"}, {"n": "report", "t": "ReportPDU"}]},
    {"def": "Message", "class": "Sequence", "fields": [
        {"n": "version", "t": {"t": "Integer", "named": [["version-1", 0], ["version-2c", 1]]}},
        {"n": "community", "t": "OctetString"},
        {"n": "data", "t": "PDUs"}]},
    # RFC 4511: LDAP, with a two-level Filter as pyasn1-modules' rfc2251
    # builds it.
    {"def": "LDAPString", "class": "OctetString"},
    {"def": "LDAPDN", "class": "LDAPString"},
    {"def": "AttributeDescription", "class": "LDAPString"},
    {"def": "AssertionValue", "class": "OctetString"},
    {"def": "AttributeValueAssertion", "class": "Sequence", "fields": [
        {"n": "attributeDesc", "t": "AttributeDescription"}, {"n": "assertionValue", "t": "AssertionValue"}]},
    {"def": "SubstringFilter", "class": "Sequence", "fields": [
        {"n": "type", "t": "AttributeDescription"},
        {"n": "substrings", "t": {"t": "SequenceOf", "of": {"t": "Choice", "fields": [
            {"n": "initial", "t": {"t": "LDAPString", "impl": ["context", 0]}},
            {"n": "any", "t": {"t": "LDAPString", "impl": ["context", 1]}},
            {"n": "final", "t": {"t": "LDAPString", "impl": ["context", 2]}}]}}}]},
    {"def": "Filter2", "class": "Choice", "fields": [
        {"n": "equalityMatch", "t": {"t": "AttributeValueAssertion", "impl": ["context", 3]}},
        {"n": "substrings", "t": {"t": "SubstringFilter", "impl": ["context", 4]}},
        {"n": "greaterOrEqual", "t": {"t": "AttributeValueAssertion", "impl": ["context", 5]}},
        {"n": "lessOrEqual", "t": {"t": "AttributeValueAssertion", "impl": ["context", 6]}},
        {"n": "present", "t": {"t": "AttributeDescription", "impl": ["context", 7]}}]},
    {"def": "Filter", "class": "Choice", "fields": [
        {"n": "and", "t": {"t": "SetOf", "of": "Filter2", "impl": ["context", 0]}},
        {"n": "or", "t": {"t": "SetOf", "of": "Filter2", "impl": ["context", 1]}},
        {"n": "not", "t": {"t": "Filter2", "expl": ["context", 2]}},
        {"n": "equalityMatch", "t": {"t": "AttributeValueAssertion", "impl": ["context", 3]}},
        {"n": "substrings", "t": {"t": "SubstringFilter", "impl": ["context", 4]}},
        {"n": "greaterOrEqual", "t": {"t": "AttributeValueAssertion", "impl": ["context", 5]}},
        {"n": "lessOrEqual", "t": {"t": "AttributeValueAssertion", "impl": ["context", 6]}},
        {"n": "present", "t": {"t": "AttributeDescription", "impl": ["context", 7]}}]},
    {"def": "AttributeSelection", "class": "SequenceOf", "of": "LDAPString"},
    {"def": "SaslCredentials", "class": "Sequence", "fields": [
        {"n": "mechanism", "t": "LDAPString"}, {"n": "credentials", "t": "OctetString", "opt": True}]},
    {"def": "AuthenticationChoice", "class": "Choice", "fields": [
        {"n": "simple", "t": {"t": "OctetString", "impl": ["context", 0]}},
        {"n": "sasl", "t": {"t": "SaslCredentials", "impl": ["context", 3]}}]},
    {"def": "BindRequest", "class": "Sequence", "tag": {"impl": ["application", 0]}, "fields": [
        {"n": "version", "t": {"t": "Integer", "sub": [{"range": [1, 127]}]}},
        {"n": "name", "t": "LDAPDN"},
        {"n": "authentication", "t": "AuthenticationChoice"}]},
    {"def": "ResultCode", "class": "Enumerated", "named": [
        ["success", 0], ["operationsError", 1], ["protocolError", 2], ["timeLimitExceeded", 3],
        ["sizeLimitExceeded", 4], ["compareFalse", 5], ["compareTrue", 6],
        ["authMethodNotSupported", 7], ["strongerAuthRequired", 8], ["referral", 10],
        ["noSuchAttribute", 16], ["noSuchObject", 32], ["invalidDNSyntax", 34],
        ["inappropriateAuthentication", 48], ["invalidCredentials", 49],
        ["insufficientAccessRights", 50], ["busy", 51], ["unavailable", 52],
        ["unwillingToPerform", 53], ["other", 80]]},
    {"def": "LDAPResult", "class": "Sequence", "fields": [
        {"n": "resultCode", "t": "ResultCode"}, {"n": "matchedDN", "t": "LDAPDN"},
        {"n": "diagnosticMessage", "t": "LDAPString"},
        {"n": "referral", "t": {"t": "SequenceOf", "of": "LDAPString", "impl": ["context", 3]}, "opt": True}]},
    {"def": "BindResponse", "class": "Sequence", "tag": {"impl": ["application", 1]}, "fields": [
        {"n": "resultCode", "t": "ResultCode"}, {"n": "matchedDN", "t": "LDAPDN"},
        {"n": "diagnosticMessage", "t": "LDAPString"},
        {"n": "referral", "t": {"t": "SequenceOf", "of": "LDAPString", "impl": ["context", 3]}, "opt": True},
        {"n": "serverSaslCreds", "t": {"t": "OctetString", "impl": ["context", 7]}, "opt": True}]},
    {"def": "UnbindRequest", "class": "Null", "tag": {"impl": ["application", 2]}},
    {"def": "SearchRequest", "class": "Sequence", "tag": {"impl": ["application", 3]}, "fields": [
        {"n": "baseObject", "t": "LDAPDN"},
        {"n": "scope", "t": {"t": "Enumerated", "named": [["baseObject", 0], ["singleLevel", 1], ["wholeSubtree", 2]]}},
        {"n": "derefAliases", "t": {"t": "Enumerated", "named": [
            ["neverDerefAliases", 0], ["derefInSearching", 1], ["derefFindingBaseObj", 2], ["derefAlways", 3]]}},
        {"n": "sizeLimit", "t": {"t": "Integer", "sub": [{"range": [0, 2147483647]}]}},
        {"n": "timeLimit", "t": {"t": "Integer", "sub": [{"range": [0, 2147483647]}]}},
        {"n": "typesOnly", "t": "Boolean"},
        {"n": "filter", "t": "Filter"},
        {"n": "attributes", "t": "AttributeSelection"}]},
    {"def": "PartialAttribute", "class": "Sequence", "fields": [
        {"n": "type", "t": "AttributeDescription"},
        {"n": "vals", "t": {"t": "SetOf", "of": "OctetString"}}]},
    {"def": "SearchResultEntry", "class": "Sequence", "tag": {"impl": ["application", 4]}, "fields": [
        {"n": "objectName", "t": "LDAPDN"},
        {"n": "attributes", "t": {"t": "SequenceOf", "of": "PartialAttribute"}}]},
    {"def": "SearchResultDone", "class": "LDAPResult", "tag": {"impl": ["application", 5]}},
    {"def": "Control", "class": "Sequence", "fields": [
        {"n": "controlType", "t": "LDAPString"},
        {"n": "criticality", "t": {"t": "Boolean", "value": False}, "default": True},
        {"n": "controlValue", "t": "OctetString", "opt": True}]},
    {"def": "ProtocolOp", "class": "Choice", "fields": [
        {"n": "bindRequest", "t": "BindRequest"}, {"n": "bindResponse", "t": "BindResponse"},
        {"n": "unbindRequest", "t": "UnbindRequest"}, {"n": "searchRequest", "t": "SearchRequest"},
        {"n": "searchResEntry", "t": "SearchResultEntry"}, {"n": "searchResDone", "t": "SearchResultDone"}]},
    {"def": "LDAPMessage", "class": "Sequence", "fields": [
        {"n": "messageID", "t": {"t": "Integer", "sub": [{"range": [0, 2147483647]}]}},
        {"n": "protocolOp", "t": "ProtocolOp"},
        {"n": "controls", "t": {"t": "SequenceOf", "of": "Control", "impl": ["context", 0]}, "opt": True}]},
    # Small types the job list leans on.
    {"def": "Colour", "class": "Enumerated", "named": [["red", 0], ["green", 1], ["blue", 2]]},
    {"def": "Percent", "class": "Integer", "cons": [{"range": [0, 100]}]},
    {"def": "Flags", "class": "BitString", "named": [["urgent", 0], ["active", 1], ["deleted", 4]]},
    {"def": "Digits", "class": "NumericString", "cons": [{"size": [1, 8]}, {"alpha": "0123456789 "}]},
    {"def": "Port", "class": "Integer", "cons": [{"union": [{"range": [1, 1023]}, {"single": [8080, 8443]}]}]},
    {"def": "NotZero", "class": "Integer", "cons": [{"excl": {"single": [0]}}]},
    {"def": "Point", "class": "Sequence", "fields": [
        {"n": "x", "t": "Integer"}, {"n": "y", "t": "Integer"},
        {"n": "label", "t": "UTF8String", "opt": True}]},
    {"def": "Shape", "class": "Choice", "fields": [
        {"n": "point", "t": {"t": "Point", "impl": ["context", 0]}},
        {"n": "circle", "t": {"t": "Sequence", "impl": ["context", 1], "fields": [
            {"n": "centre", "t": "Point"}, {"n": "radius", "t": "Integer"}]}},
        {"n": "polygon", "t": {"t": "SequenceOf", "of": "Point", "impl": ["context", 2]}}]},
    {"def": "Record", "class": "Set", "fields": [
        {"n": "id", "t": "Integer"},
        {"n": "name", "t": {"t": "UTF8String", "impl": ["context", 0]}},
        {"n": "tags", "t": {"t": "SetOf", "of": "IA5String", "impl": ["context", 1]}, "opt": True},
        {"n": "active", "t": {"t": "Boolean", "value": True}, "default": True},
        {"n": "colour", "t": "Colour", "opt": True}]},
    {"def": "Envelope", "class": "Sequence", "fields": [
        {"n": "kind", "t": "Integer"},
        {"n": "body", "t": "Any", "open": ["kind", []]}]},
]
