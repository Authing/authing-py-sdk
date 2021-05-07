QUERY = {
'addMember': """
mutation addMember($page: Int, $limit: Int, $sortBy: SortByEnum, $includeChildrenNodes: Boolean, $nodeId: String, $orgId: String, $nodeCode: String, $userIds: [String!]!, $isLeader: Boolean) {
  addMember(nodeId: $nodeId, orgId: $orgId, nodeCode: $nodeCode, userIds: $userIds, isLeader: $isLeader) {
    id
    orgId
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    path
    createdAt
    updatedAt
    children
    users(page: $page, limit: $limit, sortBy: $sortBy, includeChildrenNodes: $includeChildrenNodes) {
      totalCount
      list {
        id
        arn
        userPoolId
        username
        status
        email
        emailVerified
        phone
        phoneVerified
        unionid
        openid
        nickname
        registerSource
        photo
        password
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        browser
        company
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        city
        province
        country
        createdAt
        updatedAt
        externalId
      }
    }
  }
}

""",
'addNode': """
mutation addNode($orgId: String!, $parentNodeId: String, $name: String!, $nameI18n: String, $description: String, $descriptionI18n: String, $order: Int, $code: String) {
  addNode(orgId: $orgId, parentNodeId: $parentNodeId, name: $name, nameI18n: $nameI18n, description: $description, descriptionI18n: $descriptionI18n, order: $order, code: $code) {
    id
    rootNode {
      id
      orgId
      name
      nameI18n
      description
      descriptionI18n
      order
      code
      root
      depth
      path
      createdAt
      updatedAt
      children
    }
    nodes {
      id
      orgId
      name
      nameI18n
      description
      descriptionI18n
      order
      code
      root
      depth
      path
      createdAt
      updatedAt
      children
    }
  }
}

""",
'addNodeV2': """
mutation addNodeV2($orgId: String!, $parentNodeId: String, $name: String!, $nameI18n: String, $description: String, $descriptionI18n: String, $order: Int, $code: String) {
  addNodeV2(orgId: $orgId, parentNodeId: $parentNodeId, name: $name, nameI18n: $nameI18n, description: $description, descriptionI18n: $descriptionI18n, order: $order, code: $code) {
    id
    orgId
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    path
    createdAt
    updatedAt
    children
  }
}

""",
'addPolicyAssignments': """
mutation addPolicyAssignments($policies: [String!]!, $targetType: PolicyAssignmentTargetType!, $targetIdentifiers: [String!], $inheritByChildren: Boolean, $namespace: String) {
  addPolicyAssignments(policies: $policies, targetType: $targetType, targetIdentifiers: $targetIdentifiers, inheritByChildren: $inheritByChildren, namespace: $namespace) {
    message
    code
  }
}

""",
'addUserToGroup': """
mutation addUserToGroup($userIds: [String!]!, $code: String) {
  addUserToGroup(userIds: $userIds, code: $code) {
    message
    code
  }
}

""",
'addWhitelist': """
mutation addWhitelist($type: WhitelistType!, $list: [String!]!) {
  addWhitelist(type: $type, list: $list) {
    createdAt
    updatedAt
    value
  }
}

""",
'allow': """
mutation allow($resource: String!, $action: String!, $userId: String, $userIds: [String!], $roleCode: String, $roleCodes: [String!], $namespace: String) {
  allow(resource: $resource, action: $action, userId: $userId, userIds: $userIds, roleCode: $roleCode, roleCodes: $roleCodes, namespace: $namespace) {
    message
    code
  }
}

""",
'assignRole': """
mutation assignRole($namespace: String, $roleCode: String, $roleCodes: [String], $userIds: [String!], $groupCodes: [String!], $nodeCodes: [String!]) {
  assignRole(namespace: $namespace, roleCode: $roleCode, roleCodes: $roleCodes, userIds: $userIds, groupCodes: $groupCodes, nodeCodes: $nodeCodes) {
    message
    code
  }
}

""",
'authorizeResource': """
mutation authorizeResource($namespace: String, $resource: String, $resourceType: ResourceType, $opts: [AuthorizeResourceOpt]) {
  authorizeResource(namespace: $namespace, resource: $resource, resourceType: $resourceType, opts: $opts) {
    code
    message
  }
}

""",
'bindEmail': """
mutation bindEmail($email: String!, $emailCode: String!) {
  bindEmail(email: $email, emailCode: $emailCode) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
  }
}

""",
'bindPhone': """
mutation bindPhone($phone: String!, $phoneCode: String!) {
  bindPhone(phone: $phone, phoneCode: $phoneCode) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
  }
}

""",
'changeMfa': """
mutation changeMfa($enable: Boolean, $id: String, $userId: String, $userPoolId: String, $refresh: Boolean) {
  changeMfa(enable: $enable, id: $id, userId: $userId, userPoolId: $userPoolId, refresh: $refresh) {
    id
    userId
    userPoolId
    enable
    secret
  }
}

""",
'configEmailTemplate': """
mutation configEmailTemplate($input: ConfigEmailTemplateInput!) {
  configEmailTemplate(input: $input) {
    type
    name
    subject
    sender
    content
    redirectTo
    hasURL
    expiresIn
    enabled
    isSystem
  }
}

""",
'createFunction': """
mutation createFunction($input: CreateFunctionInput!) {
  createFunction(input: $input) {
    id
    name
    sourceCode
    description
    url
  }
}

""",
'createGroup': """
mutation createGroup($code: String!, $name: String!, $description: String) {
  createGroup(code: $code, name: $name, description: $description) {
    code
    name
    description
    createdAt
    updatedAt
  }
}

""",
'createOrg': """
mutation createOrg($name: String!, $code: String, $description: String) {
  createOrg(name: $name, code: $code, description: $description) {
    id
    rootNode {
      id
      orgId
      name
      nameI18n
      description
      descriptionI18n
      order
      code
      root
      depth
      path
      createdAt
      updatedAt
      children
    }
    nodes {
      id
      orgId
      name
      nameI18n
      description
      descriptionI18n
      order
      code
      root
      depth
      path
      createdAt
      updatedAt
      children
    }
  }
}

""",
'createPolicy': """
mutation createPolicy($namespace: String, $code: String!, $description: String, $statements: [PolicyStatementInput!]!) {
  createPolicy(namespace: $namespace, code: $code, description: $description, statements: $statements) {
    namespace
    code
    isDefault
    description
    statements {
      resource
      actions
      effect
      condition {
        param
        operator
        value
      }
    }
    createdAt
    updatedAt
    assignmentsCount
  }
}

""",
'createRole': """
mutation createRole($namespace: String, $code: String!, $description: String, $parent: String) {
  createRole(namespace: $namespace, code: $code, description: $description, parent: $parent) {
    id
    namespace
    code
    arn
    description
    createdAt
    updatedAt
    parent {
      namespace
      code
      arn
      description
      createdAt
      updatedAt
    }
  }
}

""",
'createSocialConnectionInstance': """
mutation createSocialConnectionInstance($input: CreateSocialConnectionInstanceInput!) {
  createSocialConnectionInstance(input: $input) {
    provider
    enabled
    fields {
      key
      value
    }
  }
}

""",
'createUser': """
mutation createUser($userInfo: CreateUserInput!, $keepPassword: Boolean) {
  createUser(userInfo: $userInfo, keepPassword: $keepPassword) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'createUserWithCustomData': """
mutation createUserWithCustomData($userInfo: CreateUserInput!, $keepPassword: Boolean, $params: String) {
  createUser(userInfo: $userInfo, keepPassword: $keepPassword, params: $params) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
    customData {
      key
      value
      dataType
      label
    }
  }
}

""",
'createUserpool': """
mutation createUserpool($name: String!, $domain: String!, $description: String, $logo: String, $userpoolTypes: [String!]) {
  createUserpool(name: $name, domain: $domain, description: $description, logo: $logo, userpoolTypes: $userpoolTypes) {
    id
    name
    domain
    description
    secret
    jwtSecret
    userpoolTypes {
      code
      name
      description
      image
      sdks
    }
    logo
    createdAt
    updatedAt
    emailVerifiedDefault
    sendWelcomeEmail
    registerDisabled
    appSsoEnabled
    showWxQRCodeWhenRegisterDisabled
    allowedOrigins
    tokenExpiresAfter
    isDeleted
    frequentRegisterCheck {
      timeInterval
      limit
      enabled
    }
    loginFailCheck {
      timeInterval
      limit
      enabled
    }
    changePhoneStrategy {
      verifyOldPhone
    }
    changeEmailStrategy {
      verifyOldEmail
    }
    qrcodeLoginStrategy {
      qrcodeExpiresAfter
      returnFullUserInfo
      allowExchangeUserInfoFromBrowser
      ticketExpiresAfter
    }
    app2WxappLoginStrategy {
      ticketExpriresAfter
      ticketExchangeUserInfoNeedSecret
    }
    whitelist {
      phoneEnabled
      emailEnabled
      usernameEnabled
    }
    customSMSProvider {
      enabled
      provider
    }
    packageType
  }
}

""",
'deleteFunction': """
mutation deleteFunction($id: String!) {
  deleteFunction(id: $id) {
    message
    code
  }
}

""",
'deleteGroups': """
mutation deleteGroups($codeList: [String!]!) {
  deleteGroups(codeList: $codeList) {
    message
    code
  }
}

""",
'deleteNode': """
mutation deleteNode($orgId: String!, $nodeId: String!) {
  deleteNode(orgId: $orgId, nodeId: $nodeId) {
    message
    code
  }
}

""",
'deleteOrg': """
mutation deleteOrg($id: String!) {
  deleteOrg(id: $id) {
    message
    code
  }
}

""",
'deletePolicies': """
mutation deletePolicies($codeList: [String!]!, $namespace: String) {
  deletePolicies(codeList: $codeList, namespace: $namespace) {
    message
    code
  }
}

""",
'deletePolicy': """
mutation deletePolicy($code: String!, $namespace: String) {
  deletePolicy(code: $code, namespace: $namespace) {
    message
    code
  }
}

""",
'deleteRole': """
mutation deleteRole($code: String!, $namespace: String) {
  deleteRole(code: $code, namespace: $namespace) {
    message
    code
  }
}

""",
'deleteRoles': """
mutation deleteRoles($codeList: [String!]!, $namespace: String) {
  deleteRoles(codeList: $codeList, namespace: $namespace) {
    message
    code
  }
}

""",
'deleteUser': """
mutation deleteUser($id: String!) {
  deleteUser(id: $id) {
    message
    code
  }
}

""",
'deleteUserpool': """
mutation deleteUserpool {
  deleteUserpool {
    message
    code
  }
}

""",
'deleteUsers': """
mutation deleteUsers($ids: [String!]!) {
  deleteUsers(ids: $ids) {
    message
    code
  }
}

""",
'disableEmailTemplate': """
mutation disableEmailTemplate($type: EmailTemplateType!) {
  disableEmailTemplate(type: $type) {
    type
    name
    subject
    sender
    content
    redirectTo
    hasURL
    expiresIn
    enabled
    isSystem
  }
}

""",
'disableSocialConnectionInstance': """
mutation disableSocialConnectionInstance($provider: String!) {
  disableSocialConnectionInstance(provider: $provider) {
    provider
    enabled
    fields {
      key
      value
    }
  }
}

""",
'disbalePolicyAssignment': """
mutation disbalePolicyAssignment($policy: String!, $targetType: PolicyAssignmentTargetType!, $targetIdentifier: String!, $namespace: String) {
  disbalePolicyAssignment(policy: $policy, targetType: $targetType, targetIdentifier: $targetIdentifier, namespace: $namespace) {
    message
    code
  }
}

""",
'enableEmailTemplate': """
mutation enableEmailTemplate($type: EmailTemplateType!) {
  enableEmailTemplate(type: $type) {
    type
    name
    subject
    sender
    content
    redirectTo
    hasURL
    expiresIn
    enabled
    isSystem
  }
}

""",
'enablePolicyAssignment': """
mutation enablePolicyAssignment($policy: String!, $targetType: PolicyAssignmentTargetType!, $targetIdentifier: String!, $namespace: String) {
  enablePolicyAssignment(policy: $policy, targetType: $targetType, targetIdentifier: $targetIdentifier, namespace: $namespace) {
    message
    code
  }
}

""",
'enableSocialConnectionInstance': """
mutation enableSocialConnectionInstance($provider: String!) {
  enableSocialConnectionInstance(provider: $provider) {
    provider
    enabled
    fields {
      key
      value
    }
  }
}

""",
'loginByEmail': """
mutation loginByEmail($input: LoginByEmailInput!) {
  loginByEmail(input: $input) {
    id
    arn
    status
    userPoolId
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'loginByPhoneCode': """
mutation loginByPhoneCode($input: LoginByPhoneCodeInput!) {
  loginByPhoneCode(input: $input) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'loginByPhonePassword': """
mutation loginByPhonePassword($input: LoginByPhonePasswordInput!) {
  loginByPhonePassword(input: $input) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'loginBySubAccount': """
mutation loginBySubAccount($account: String!, $password: String!, $captchaCode: String, $clientIp: String) {
  loginBySubAccount(account: $account, password: $password, captchaCode: $captchaCode, clientIp: $clientIp) {
    id
    arn
    status
    userPoolId
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'loginByUsername': """
mutation loginByUsername($input: LoginByUsernameInput!) {
  loginByUsername(input: $input) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'moveNode': """
mutation moveNode($orgId: String!, $nodeId: String!, $targetParentId: String!) {
  moveNode(orgId: $orgId, nodeId: $nodeId, targetParentId: $targetParentId) {
    id
    rootNode {
      id
      orgId
      name
      nameI18n
      description
      descriptionI18n
      order
      code
      root
      depth
      path
      createdAt
      updatedAt
      children
    }
    nodes {
      id
      orgId
      name
      nameI18n
      description
      descriptionI18n
      order
      code
      root
      depth
      path
      createdAt
      updatedAt
      children
    }
  }
}

""",
'refreshAccessToken': """
mutation refreshAccessToken($accessToken: String) {
  refreshAccessToken(accessToken: $accessToken) {
    accessToken
    exp
    iat
  }
}

""",
'refreshToken': """
mutation refreshToken($id: String) {
  refreshToken(id: $id) {
    token
    iat
    exp
  }
}

""",
'refreshUserpoolSecret': """
mutation refreshUserpoolSecret {
  refreshUserpoolSecret
}

""",
'registerByEmail': """
mutation registerByEmail($input: RegisterByEmailInput!) {
  registerByEmail(input: $input) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'registerByPhoneCode': """
mutation registerByPhoneCode($input: RegisterByPhoneCodeInput!) {
  registerByPhoneCode(input: $input) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'registerByUsername': """
mutation registerByUsername($input: RegisterByUsernameInput!) {
  registerByUsername(input: $input) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'removeMember': """
mutation removeMember($page: Int, $limit: Int, $sortBy: SortByEnum, $includeChildrenNodes: Boolean, $nodeId: String, $orgId: String, $nodeCode: String, $userIds: [String!]!) {
  removeMember(nodeId: $nodeId, orgId: $orgId, nodeCode: $nodeCode, userIds: $userIds) {
    id
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    createdAt
    updatedAt
    children
    users(page: $page, limit: $limit, sortBy: $sortBy, includeChildrenNodes: $includeChildrenNodes) {
      totalCount
      list {
        id
        arn
        userPoolId
        status
        username
        email
        emailVerified
        phone
        phoneVerified
        unionid
        openid
        nickname
        registerSource
        photo
        password
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        browser
        company
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        city
        province
        country
        createdAt
        updatedAt
      }
    }
  }
}

""",
'removePolicyAssignments': """
mutation removePolicyAssignments($policies: [String!]!, $targetType: PolicyAssignmentTargetType!, $targetIdentifiers: [String!], $namespace: String) {
  removePolicyAssignments(policies: $policies, targetType: $targetType, targetIdentifiers: $targetIdentifiers, namespace: $namespace) {
    message
    code
  }
}

""",
'removeUdf': """
mutation removeUdf($targetType: UDFTargetType!, $key: String!) {
  removeUdf(targetType: $targetType, key: $key) {
    message
    code
  }
}

""",
'removeUdv': """
mutation removeUdv($targetType: UDFTargetType!, $targetId: String!, $key: String!) {
  removeUdv(targetType: $targetType, targetId: $targetId, key: $key) {
    key
    dataType
    value
    label
  }
}

""",
'removeUserFromGroup': """
mutation removeUserFromGroup($userIds: [String!]!, $code: String) {
  removeUserFromGroup(userIds: $userIds, code: $code) {
    message
    code
  }
}

""",
'removeWhitelist': """
mutation removeWhitelist($type: WhitelistType!, $list: [String!]!) {
  removeWhitelist(type: $type, list: $list) {
    createdAt
    updatedAt
    value
  }
}

""",
'resetPassword': """
mutation resetPassword($phone: String, $email: String, $code: String!, $newPassword: String!) {
  resetPassword(phone: $phone, email: $email, code: $code, newPassword: $newPassword) {
    message
    code
  }
}

""",
'revokeRole': """
mutation revokeRole($namespace: String, $roleCode: String, $roleCodes: [String], $userIds: [String!], $groupCodes: [String!], $nodeCodes: [String!]) {
  revokeRole(namespace: $namespace, roleCode: $roleCode, roleCodes: $roleCodes, userIds: $userIds, groupCodes: $groupCodes, nodeCodes: $nodeCodes) {
    message
    code
  }
}

""",
'sendEmail': """
mutation sendEmail($email: String!, $scene: EmailScene!) {
  sendEmail(email: $email, scene: $scene) {
    message
    code
  }
}

""",
'setMainDepartment': """
mutation setMainDepartment($userId: String!, $departmentId: String) {
  setMainDepartment(userId: $userId, departmentId: $departmentId) {
    message
    code
  }
}

""",
'setUdf': """
mutation setUdf($targetType: UDFTargetType!, $key: String!, $dataType: UDFDataType!, $label: String!, $options: String) {
  setUdf(targetType: $targetType, key: $key, dataType: $dataType, label: $label, options: $options) {
    targetType
    dataType
    key
    label
    options
  }
}

""",
'setUdfValueBatch': """
mutation setUdfValueBatch($targetType: UDFTargetType!, $input: [SetUdfValueBatchInput!]!) {
  setUdfValueBatch(targetType: $targetType, input: $input) {
    code
    message
  }
}

""",
'setUdv': """
mutation setUdv($targetType: UDFTargetType!, $targetId: String!, $key: String!, $value: String!) {
  setUdv(targetType: $targetType, targetId: $targetId, key: $key, value: $value) {
    key
    dataType
    value
    label
  }
}

""",
'setUdvBatch': """
mutation setUdvBatch($targetType: UDFTargetType!, $targetId: String!, $udvList: [UserDefinedDataInput!]) {
  setUdvBatch(targetType: $targetType, targetId: $targetId, udvList: $udvList) {
    key
    dataType
    value
    label
  }
}

""",
'unbindEmail': """
mutation unbindEmail {
  unbindEmail {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
  }
}

""",
'unbindPhone': """
mutation unbindPhone {
  unbindPhone {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
  }
}

""",
'updateEmail': """
mutation updateEmail($email: String!, $emailCode: String!, $oldEmail: String, $oldEmailCode: String) {
  updateEmail(email: $email, emailCode: $emailCode, oldEmail: $oldEmail, oldEmailCode: $oldEmailCode) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
  }
}

""",
'updateFunction': """
mutation updateFunction($input: UpdateFunctionInput!) {
  updateFunction(input: $input) {
    id
    name
    sourceCode
    description
    url
  }
}

""",
'updateGroup': """
mutation updateGroup($code: String!, $name: String, $description: String, $newCode: String) {
  updateGroup(code: $code, name: $name, description: $description, newCode: $newCode) {
    code
    name
    description
    createdAt
    updatedAt
  }
}

""",
'updateNode': """
mutation updateNode($page: Int, $limit: Int, $sortBy: SortByEnum, $includeChildrenNodes: Boolean, $id: String!, $name: String, $code: String, $description: String) {
  updateNode(id: $id, name: $name, code: $code, description: $description) {
    id
    orgId
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    path
    createdAt
    updatedAt
    children
    users(page: $page, limit: $limit, sortBy: $sortBy, includeChildrenNodes: $includeChildrenNodes) {
      totalCount
    }
  }
}

""",
'updatePassword': """
mutation updatePassword($newPassword: String!, $oldPassword: String) {
  updatePassword(newPassword: $newPassword, oldPassword: $oldPassword) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
  }
}

""",
'updatePhone': """
mutation updatePhone($phone: String!, $phoneCode: String!, $oldPhone: String, $oldPhoneCode: String) {
  updatePhone(phone: $phone, phoneCode: $phoneCode, oldPhone: $oldPhone, oldPhoneCode: $oldPhoneCode) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
  }
}

""",
'updatePolicy': """
mutation updatePolicy($namespace: String, $code: String!, $description: String, $statements: [PolicyStatementInput!], $newCode: String) {
  updatePolicy(namespace: $namespace, code: $code, description: $description, statements: $statements, newCode: $newCode) {
    namespace
    code
    description
    statements {
      resource
      actions
      effect
      condition {
        param
        operator
        value
      }
    }
    createdAt
    updatedAt
  }
}

""",
'updateRole': """
mutation updateRole($code: String!, $description: String, $newCode: String, $namespace: String) {
  updateRole(code: $code, description: $description, newCode: $newCode, namespace: $namespace) {
    id
    namespace
    code
    arn
    description
    createdAt
    updatedAt
    parent {
      namespace
      code
      arn
      description
      createdAt
      updatedAt
    }
  }
}

""",
'updateUser': """
mutation updateUser($id: String, $input: UpdateUserInput!) {
  updateUser(id: $id, input: $input) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'updateUserpool': """
mutation updateUserpool($input: UpdateUserpoolInput!) {
  updateUserpool(input: $input) {
    id
    name
    domain
    description
    secret
    jwtSecret
    userpoolTypes {
      code
      name
      description
      image
      sdks
    }
    logo
    createdAt
    updatedAt
    emailVerifiedDefault
    sendWelcomeEmail
    registerDisabled
    appSsoEnabled
    showWxQRCodeWhenRegisterDisabled
    allowedOrigins
    tokenExpiresAfter
    isDeleted
    frequentRegisterCheck {
      timeInterval
      limit
      enabled
    }
    loginFailCheck {
      timeInterval
      limit
      enabled
    }
    changePhoneStrategy {
      verifyOldPhone
    }
    changeEmailStrategy {
      verifyOldEmail
    }
    qrcodeLoginStrategy {
      qrcodeExpiresAfter
      returnFullUserInfo
      allowExchangeUserInfoFromBrowser
      ticketExpiresAfter
    }
    app2WxappLoginStrategy {
      ticketExpriresAfter
      ticketExchangeUserInfoNeedSecret
    }
    whitelist {
      phoneEnabled
      emailEnabled
      usernameEnabled
    }
    customSMSProvider {
      enabled
      provider
      config
    }
    packageType
    useCustomUserStore
    loginRequireEmailVerified
    verifyCodeLength
  }
}

""",
'accessToken': """
query accessToken($userPoolId: String!, $secret: String!) {
  accessToken(userPoolId: $userPoolId, secret: $secret) {
    accessToken
    exp
    iat
  }
}

""",
'archivedUsers': """
query archivedUsers($page: Int, $limit: Int) {
  archivedUsers(page: $page, limit: $limit) {
    totalCount
    list {
      id
      arn
      status
      userPoolId
      username
      email
      emailVerified
      phone
      phoneVerified
      unionid
      openid
      nickname
      registerSource
      photo
      password
      oauth
      token
      tokenExpiredAt
      loginsCount
      lastLogin
      lastIP
      signedUp
      blocked
      isDeleted
      device
      browser
      company
      name
      givenName
      familyName
      middleName
      profile
      preferredUsername
      website
      gender
      birthdate
      zoneinfo
      locale
      address
      formatted
      streetAddress
      locality
      region
      postalCode
      city
      province
      country
      createdAt
      updatedAt
      externalId
    }
  }
}

""",
'authorizedTargets': """
query authorizedTargets($namespace: String!, $resourceType: ResourceType!, $resource: String!, $targetType: PolicyAssignmentTargetType, $actions: AuthorizedTargetsActionsInput) {
  authorizedTargets(namespace: $namespace, resource: $resource, resourceType: $resourceType, targetType: $targetType, actions: $actions) {
    totalCount
    list {
      targetType
      targetIdentifier
      actions
    }
  }
}

""",
'checkLoginStatus': """
query checkLoginStatus($token: String) {
  checkLoginStatus(token: $token) {
    code
    message
    status
    exp
    iat
    data {
      id
      userPoolId
      arn
    }
  }
}

""",
'checkPasswordStrength': """
query checkPasswordStrength($password: String!) {
  checkPasswordStrength(password: $password) {
    valid
    message
  }
}

""",
'childrenNodes': """
query childrenNodes($orgId: String!, $nodeId: String!) {
  childrenNodes(orgId: $orgId, nodeId: $nodeId) {
    id
    orgId
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    path
    createdAt
    updatedAt
    children
  }
}

""",
'emailTemplates': """
query emailTemplates {
  emailTemplates {
    type
    name
    subject
    sender
    content
    redirectTo
    hasURL
    expiresIn
    enabled
    isSystem
  }
}

""",
'findUser': """
query findUser($email: String, $phone: String, $username: String, $externalId: String) {
  findUser(email: $email, phone: $phone, username: $username, externalId: $externalId) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'findUserWithCustomData': """
query findUserWithCustomData($email: String, $phone: String, $username: String, $externalId: String) {
  findUser(email: $email, phone: $phone, username: $username, externalId: $externalId) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
    customData {
      key
      value
      dataType
      label
    }
  }
}

""",
'function': """
query function($id: String) {
  function(id: $id) {
    id
    name
    sourceCode
    description
    url
  }
}

""",
'functions': """
query functions($page: Int, $limit: Int, $sortBy: SortByEnum) {
  functions(page: $page, limit: $limit, sortBy: $sortBy) {
    list {
      id
      name
      sourceCode
      description
      url
    }
    totalCount
  }
}

""",
'getUserDepartments': """
query getUserDepartments($id: String!, $orgId: String) {
  user(id: $id) {
    departments(orgId: $orgId) {
      totalCount
      list {
        department {
          id
          orgId
          name
          nameI18n
          description
          descriptionI18n
          order
          code
          root
          depth
          path
          codePath
          namePath
          createdAt
          updatedAt
          children
        }
        isMainDepartment
        joinedAt
      }
    }
  }
}

""",
'getUserGroups': """
query getUserGroups($id: String!) {
  user(id: $id) {
    groups {
      totalCount
      list {
        code
        name
        description
        createdAt
        updatedAt
      }
    }
  }
}

""",
'getUserRoles': """
query getUserRoles($id: String!, $namespace: String) {
  user(id: $id) {
    roles(namespace: $namespace) {
      totalCount
      list {
        code
        namespace
        arn
        description
        createdAt
        updatedAt
        parent {
          code
          namespace
          arn
          description
          createdAt
          updatedAt
        }
      }
    }
  }
}

""",
'group': """
query group($code: String!) {
  group(code: $code) {
    code
    name
    description
    createdAt
    updatedAt
  }
}

""",
'groupWithUsers': """
query groupWithUsers($code: String!, $page: Int, $limit: Int) {
  group(code: $code) {
    users(page: $page, limit: $limit) {
      totalCount
      list {
        id
        arn
        userPoolId
        username
        email
        emailVerified
        phone
        phoneVerified
        unionid
        openid
        nickname
        registerSource
        photo
        password
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        browser
        company
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        city
        province
        country
        createdAt
        updatedAt
        externalId
      }
    }
  }
}

""",
'groupWithUsersWithCustomData': """
query groupWithUsersWithCustomData($code: String!, $page: Int, $limit: Int) {
  group(code: $code) {
    users(page: $page, limit: $limit) {
      totalCount
      list {
        id
        arn
        userPoolId
        username
        email
        emailVerified
        phone
        phoneVerified
        unionid
        openid
        nickname
        registerSource
        photo
        password
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        browser
        company
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        city
        province
        country
        createdAt
        updatedAt
        externalId
        customData {
          key
          value
          dataType
          label
        }
      }
    }
  }
}

""",
'groups': """
query groups($userId: String, $page: Int, $limit: Int, $sortBy: SortByEnum) {
  groups(userId: $userId, page: $page, limit: $limit, sortBy: $sortBy) {
    totalCount
    list {
      code
      name
      description
      createdAt
      updatedAt
    }
  }
}

""",
'isActionAllowed': """
query isActionAllowed($resource: String!, $action: String!, $userId: String!, $namespace: String) {
  isActionAllowed(resource: $resource, action: $action, userId: $userId, namespace: $namespace)
}

""",
'isActionDenied': """
query isActionDenied($resource: String!, $action: String!, $userId: String!) {
  isActionDenied(resource: $resource, action: $action, userId: $userId)
}

""",
'isDomainAvaliable': """
query isDomainAvaliable($domain: String!) {
  isDomainAvaliable(domain: $domain)
}

""",
'isRootNode': """
query isRootNode($nodeId: String!, $orgId: String!) {
  isRootNode(nodeId: $nodeId, orgId: $orgId)
}

""",
'isUserExists': """
query isUserExists($email: String, $phone: String, $username: String, $externalId: String) {
  isUserExists(email: $email, phone: $phone, username: $username, externalId: $externalId)
}

""",
'authorizedResources': """
query authorizedResources($targetType: PolicyAssignmentTargetType, $targetIdentifier: String, $namespace: String, $resourceType: String) {
  authorizedResources(targetType: $targetType, targetIdentifier: $targetIdentifier, namespace: $namespace, resourceType: $resourceType) {
    totalCount
    list {
      code
      type
      actions
    }
  }
}

""",
'listGroupAuthorizedResources': """
query listGroupAuthorizedResources($code: String!, $namespace: String, $resourceType: String) {
  group(code: $code) {
    authorizedResources(namespace: $namespace, resourceType: $resourceType) {
      totalCount
      list {
        code
        type
        actions
      }
    }
  }
}

""",
'listNodeByCodeAuthorizedResources': """
query listNodeByCodeAuthorizedResources($orgId: String!, $code: String!, $namespace: String, $resourceType: String) {
  nodeByCode(orgId: $orgId, code: $code) {
    authorizedResources(namespace: $namespace, resourceType: $resourceType) {
      totalCount
      list {
        code
        type
        actions
      }
    }
  }
}

""",
'listNodeByIdAuthorizedResources': """
query listNodeByIdAuthorizedResources($id: String!, $namespace: String, $resourceType: String) {
  nodeById(id: $id) {
    authorizedResources(namespace: $namespace, resourceType: $resourceType) {
      totalCount
      list {
        code
        type
        actions
      }
    }
  }
}

""",
'listRoleAuthorizedResources': """
query listRoleAuthorizedResources($code: String!, $namespace: String, $resourceType: String) {
  role(code: $code, namespace: $namespace) {
    authorizedResources(resourceType: $resourceType) {
      totalCount
      list {
        code
        type
        actions
      }
    }
  }
}

""",
'listUserAuthorizedResources': """
query listUserAuthorizedResources($id: String!, $namespace: String, $resourceType: String) {
  user(id: $id) {
    authorizedResources(namespace: $namespace, resourceType: $resourceType) {
      totalCount
      list {
        code
        type
        actions
      }
    }
  }
}

""",
'nodeByCode': """
query nodeByCode($orgId: String!, $code: String!) {
  nodeByCode(orgId: $orgId, code: $code) {
    id
    orgId
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    path
    createdAt
    updatedAt
    children
  }
}

""",
'nodeByCodeWithMembers': """
query nodeByCodeWithMembers($page: Int, $limit: Int, $sortBy: SortByEnum, $includeChildrenNodes: Boolean, $orgId: String!, $code: String!) {
  nodeByCode(orgId: $orgId, code: $code) {
    id
    orgId
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    createdAt
    updatedAt
    children
    users(page: $page, limit: $limit, sortBy: $sortBy, includeChildrenNodes: $includeChildrenNodes) {
      totalCount
      list {
        id
        arn
        userPoolId
        status
        username
        email
        emailVerified
        phone
        phoneVerified
        unionid
        openid
        nickname
        registerSource
        photo
        password
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        browser
        company
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        city
        province
        country
        createdAt
        updatedAt
        externalId
      }
    }
  }
}

""",
'nodeById': """
query nodeById($id: String!) {
  nodeById(id: $id) {
    id
    orgId
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    path
    createdAt
    updatedAt
    children
  }
}

""",
'nodeByIdWithMembers': """
query nodeByIdWithMembers($page: Int, $limit: Int, $sortBy: SortByEnum, $includeChildrenNodes: Boolean, $id: String!) {
  nodeById(id: $id) {
    id
    orgId
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    createdAt
    updatedAt
    children
    users(page: $page, limit: $limit, sortBy: $sortBy, includeChildrenNodes: $includeChildrenNodes) {
      totalCount
      list {
        id
        arn
        userPoolId
        status
        username
        email
        emailVerified
        phone
        phoneVerified
        unionid
        openid
        nickname
        registerSource
        photo
        password
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        browser
        company
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        city
        province
        country
        createdAt
        updatedAt
        externalId
      }
    }
  }
}

""",
'org': """
query org($id: String!) {
  org(id: $id) {
    id
    rootNode {
      id
      orgId
      name
      nameI18n
      description
      descriptionI18n
      order
      code
      root
      depth
      path
      createdAt
      updatedAt
      children
    }
    nodes {
      id
      orgId
      name
      nameI18n
      description
      descriptionI18n
      order
      code
      root
      depth
      path
      createdAt
      updatedAt
      children
    }
  }
}

""",
'orgs': """
query orgs($page: Int, $limit: Int, $sortBy: SortByEnum) {
  orgs(page: $page, limit: $limit, sortBy: $sortBy) {
    totalCount
    list {
      id
      rootNode {
        id
        name
        nameI18n
        path
        description
        descriptionI18n
        order
        code
        root
        depth
        createdAt
        updatedAt
        children
      }
      nodes {
        id
        name
        path
        nameI18n
        description
        descriptionI18n
        order
        code
        root
        depth
        createdAt
        updatedAt
        children
      }
    }
  }
}

""",
'policies': """
query policies($page: Int, $limit: Int, $namespace: String) {
  policies(page: $page, limit: $limit, namespace: $namespace) {
    totalCount
    list {
      namespace
      code
      description
      createdAt
      updatedAt
      statements {
        resource
        actions
        effect
        condition {
          param
          operator
          value
        }
      }
    }
  }
}

""",
'policy': """
query policy($namespace: String, $code: String!) {
  policy(code: $code, namespace: $namespace) {
    namespace
    code
    isDefault
    description
    statements {
      resource
      actions
      effect
      condition {
        param
        operator
        value
      }
    }
    createdAt
    updatedAt
  }
}

""",
'policyAssignments': """
query policyAssignments($namespace: String, $code: String, $targetType: PolicyAssignmentTargetType, $targetIdentifier: String, $page: Int, $limit: Int) {
  policyAssignments(namespace: $namespace, code: $code, targetType: $targetType, targetIdentifier: $targetIdentifier, page: $page, limit: $limit) {
    totalCount
    list {
      code
      targetType
      targetIdentifier
    }
  }
}

""",
'policyWithAssignments': """
query policyWithAssignments($page: Int, $limit: Int, $code: String!) {
  policy(code: $code) {
    code
    isDefault
    description
    statements {
      resource
      actions
      effect
    }
    createdAt
    updatedAt
    assignmentsCount
    assignments(page: $page, limit: $limit) {
      code
      targetType
      targetIdentifier
    }
  }
}

""",
'previewEmail': """
query previewEmail($type: EmailTemplateType!) {
  previewEmail(type: $type)
}

""",
'qiniuUptoken': """
query qiniuUptoken($type: String) {
  qiniuUptoken(type: $type)
}

""",
'queryMfa': """
query queryMfa($id: String, $userId: String, $userPoolId: String) {
  queryMfa(id: $id, userId: $userId, userPoolId: $userPoolId) {
    id
    userId
    userPoolId
    enable
    secret
  }
}

""",
'role': """
query role($code: String!, $namespace: String) {
  role(code: $code, namespace: $namespace) {
    id
    namespace
    code
    arn
    description
    createdAt
    updatedAt
    parent {
      namespace
      code
      arn
      description
      createdAt
      updatedAt
    }
  }
}

""",
'roleWithUsers': """
query roleWithUsers($code: String!, $namespace: String, $page: Int, $limit: Int) {
  role(code: $code, namespace: $namespace) {
    users(page: $page, limit: $limit) {
      totalCount
      list {
        id
        arn
        status
        userPoolId
        username
        email
        emailVerified
        phone
        phoneVerified
        unionid
        openid
        nickname
        registerSource
        photo
        password
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        browser
        company
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        city
        province
        country
        createdAt
        updatedAt
        externalId
      }
    }
  }
}

""",
'roleWithUsersWithCustomData': """
query roleWithUsersWithCustomData($code: String!, $namespace: String, $page: Int, $limit: Int) {
  role(code: $code, namespace: $namespace) {
    users(page: $page, limit: $limit) {
      totalCount
      list {
        id
        arn
        status
        userPoolId
        username
        email
        emailVerified
        phone
        phoneVerified
        unionid
        openid
        nickname
        registerSource
        photo
        password
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        browser
        company
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        city
        province
        country
        createdAt
        updatedAt
        externalId
        customData {
          key
          value
          dataType
          label
        }
      }
    }
  }
}

""",
'roles': """
query roles($namespace: String, $page: Int, $limit: Int, $sortBy: SortByEnum) {
  roles(namespace: $namespace, page: $page, limit: $limit, sortBy: $sortBy) {
    totalCount
    list {
      id
      namespace
      code
      arn
      description
      createdAt
      updatedAt
    }
  }
}

""",
'rootNode': """
query rootNode($orgId: String!) {
  rootNode(orgId: $orgId) {
    id
    orgId
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    path
    codePath
    namePath
    createdAt
    updatedAt
    children
  }
}

""",
'searchNodes': """
query searchNodes($keyword: String!) {
  searchNodes(keyword: $keyword) {
    id
    orgId
    name
    nameI18n
    description
    descriptionI18n
    order
    code
    root
    depth
    path
    codePath
    namePath
    createdAt
    updatedAt
    children
  }
}

""",
'searchUser': """
query searchUser($query: String!, $fields: [String], $page: Int, $limit: Int, $departmentOpts: [SearchUserDepartmentOpt], $groupOpts: [SearchUserGroupOpt], $roleOpts: [SearchUserRoleOpt]) {
  searchUser(query: $query, fields: $fields, page: $page, limit: $limit, departmentOpts: $departmentOpts, groupOpts: $groupOpts, roleOpts: $roleOpts) {
    totalCount
    list {
      id
      arn
      userPoolId
      status
      username
      email
      emailVerified
      phone
      phoneVerified
      unionid
      openid
      nickname
      registerSource
      photo
      password
      oauth
      token
      tokenExpiredAt
      loginsCount
      lastLogin
      lastIP
      signedUp
      blocked
      isDeleted
      device
      browser
      company
      name
      givenName
      familyName
      middleName
      profile
      preferredUsername
      website
      gender
      birthdate
      zoneinfo
      locale
      address
      formatted
      streetAddress
      locality
      region
      postalCode
      city
      province
      country
      createdAt
      updatedAt
      externalId
    }
  }
}

""",
'searchUserWithCustomData': """
query searchUserWithCustomData($query: String!, $fields: [String], $page: Int, $limit: Int, $departmentOpts: [SearchUserDepartmentOpt], $groupOpts: [SearchUserGroupOpt], $roleOpts: [SearchUserRoleOpt]) {
  searchUser(query: $query, fields: $fields, page: $page, limit: $limit, departmentOpts: $departmentOpts, groupOpts: $groupOpts, roleOpts: $roleOpts) {
    totalCount
    list {
      id
      arn
      userPoolId
      status
      username
      email
      emailVerified
      phone
      phoneVerified
      unionid
      openid
      nickname
      registerSource
      photo
      password
      oauth
      token
      tokenExpiredAt
      loginsCount
      lastLogin
      lastIP
      signedUp
      blocked
      isDeleted
      device
      browser
      company
      name
      givenName
      familyName
      middleName
      profile
      preferredUsername
      website
      gender
      birthdate
      zoneinfo
      locale
      address
      formatted
      streetAddress
      locality
      region
      postalCode
      city
      province
      country
      createdAt
      updatedAt
      externalId
      customData {
        key
        value
        dataType
        label
      }
    }
  }
}

""",
'socialConnection': """
query socialConnection($provider: String!) {
  socialConnection(provider: $provider) {
    provider
    name
    logo
    description
    fields {
      key
      label
      type
      placeholder
    }
  }
}

""",
'socialConnectionInstance': """
query socialConnectionInstance($provider: String!) {
  socialConnectionInstance(provider: $provider) {
    provider
    enabled
    fields {
      key
      value
    }
  }
}

""",
'socialConnectionInstances': """
query socialConnectionInstances {
  socialConnectionInstances {
    provider
    enabled
    fields {
      key
      value
    }
  }
}

""",
'socialConnections': """
query socialConnections {
  socialConnections {
    provider
    name
    logo
    description
    fields {
      key
      label
      type
      placeholder
    }
  }
}

""",
'templateCode': """
query templateCode {
  templateCode
}

""",
'udf': """
query udf($targetType: UDFTargetType!) {
  udf(targetType: $targetType) {
    targetType
    dataType
    key
    label
    options
  }
}

""",
'udfValueBatch': """
query udfValueBatch($targetType: UDFTargetType!, $targetIds: [String!]!) {
  udfValueBatch(targetType: $targetType, targetIds: $targetIds) {
    targetId
    data {
      key
      dataType
      value
      label
    }
  }
}

""",
'udv': """
query udv($targetType: UDFTargetType!, $targetId: String!) {
  udv(targetType: $targetType, targetId: $targetId) {
    key
    dataType
    value
    label
  }
}

""",
'user': """
query user($id: String) {
  user(id: $id) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'userBatch': """
query userBatch($ids: [String!]!, $type: String) {
  userBatch(ids: $ids, type: $type) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
  }
}

""",
'userBatchWithCustomData': """
query userBatchWithCustomData($ids: [String!]!, $type: String) {
  userBatch(ids: $ids, type: $type) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
    customData {
      key
      value
      dataType
      label
    }
  }
}

""",
'userWithCustomData': """
query userWithCustomData($id: String) {
  user(id: $id) {
    id
    arn
    userPoolId
    status
    username
    email
    emailVerified
    phone
    phoneVerified
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
    unionid
    openid
    nickname
    registerSource
    photo
    password
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    device
    browser
    company
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    city
    province
    country
    createdAt
    updatedAt
    externalId
    customData {
      key
      value
      dataType
      label
    }
  }
}

""",
'userpool': """
query userpool {
  userpool {
    id
    name
    domain
    description
    secret
    jwtSecret
    ownerId
    userpoolTypes {
      code
      name
      description
      image
      sdks
    }
    logo
    createdAt
    updatedAt
    emailVerifiedDefault
    sendWelcomeEmail
    registerDisabled
    appSsoEnabled
    showWxQRCodeWhenRegisterDisabled
    allowedOrigins
    tokenExpiresAfter
    isDeleted
    frequentRegisterCheck {
      timeInterval
      limit
      enabled
    }
    loginFailCheck {
      timeInterval
      limit
      enabled
    }
    changePhoneStrategy {
      verifyOldPhone
    }
    changeEmailStrategy {
      verifyOldEmail
    }
    qrcodeLoginStrategy {
      qrcodeExpiresAfter
      returnFullUserInfo
      allowExchangeUserInfoFromBrowser
      ticketExpiresAfter
    }
    app2WxappLoginStrategy {
      ticketExpriresAfter
      ticketExchangeUserInfoNeedSecret
    }
    whitelist {
      phoneEnabled
      emailEnabled
      usernameEnabled
    }
    customSMSProvider {
      enabled
      provider
      config
    }
    packageType
    useCustomUserStore
    loginRequireEmailVerified
    verifyCodeLength
  }
}

""",
'userpoolTypes': """
query userpoolTypes {
  userpoolTypes {
    code
    name
    description
    image
    sdks
  }
}

""",
'userpools': """
query userpools($page: Int, $limit: Int, $sortBy: SortByEnum) {
  userpools(page: $page, limit: $limit, sortBy: $sortBy) {
    totalCount
    list {
      id
      name
      domain
      ownerId
      description
      secret
      jwtSecret
      logo
      createdAt
      updatedAt
      emailVerifiedDefault
      sendWelcomeEmail
      registerDisabled
      appSsoEnabled
      showWxQRCodeWhenRegisterDisabled
      allowedOrigins
      tokenExpiresAfter
      isDeleted
      packageType
      useCustomUserStore
      loginRequireEmailVerified
      verifyCodeLength
    }
  }
}

""",
'users': """
query users($page: Int, $limit: Int, $sortBy: SortByEnum) {
  users(page: $page, limit: $limit, sortBy: $sortBy) {
    totalCount
    list {
      id
      arn
      userPoolId
      status
      username
      email
      emailVerified
      phone
      phoneVerified
      unionid
      openid
      nickname
      registerSource
      photo
      password
      oauth
      token
      tokenExpiredAt
      loginsCount
      lastLogin
      lastIP
      signedUp
      blocked
      isDeleted
      device
      browser
      company
      name
      givenName
      familyName
      middleName
      profile
      preferredUsername
      website
      gender
      birthdate
      zoneinfo
      locale
      address
      formatted
      streetAddress
      locality
      region
      postalCode
      city
      province
      country
      createdAt
      updatedAt
      externalId
    }
  }
}

""",
'usersWithCustomData': """
query usersWithCustomData($page: Int, $limit: Int, $sortBy: SortByEnum) {
  users(page: $page, limit: $limit, sortBy: $sortBy) {
    totalCount
    list {
      id
      arn
      userPoolId
      status
      username
      email
      emailVerified
      phone
      phoneVerified
      unionid
      openid
      nickname
      registerSource
      photo
      password
      oauth
      token
      tokenExpiredAt
      loginsCount
      lastLogin
      lastIP
      signedUp
      blocked
      isDeleted
      device
      browser
      company
      name
      givenName
      familyName
      middleName
      profile
      preferredUsername
      website
      gender
      birthdate
      zoneinfo
      locale
      address
      formatted
      streetAddress
      locality
      region
      postalCode
      city
      province
      country
      createdAt
      updatedAt
      externalId
      customData {
        key
        value
        dataType
        label
      }
    }
  }
}

""",
'whitelist': """
query whitelist($type: WhitelistType!) {
  whitelist(type: $type) {
    createdAt
    updatedAt
    value
  }
}

""",
}