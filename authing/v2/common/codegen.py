QUERY = {
    'addMember': """
mutation addMember($page: Int, $limit: Int, $sortBy: SortByEnum, $includeChildrenNodes: Boolean, $nodeId: String, $orgId: String, $nodeCode: String, $userIds: [String!]!, $isLeader: Boolean) {
  addMember(nodeId: $nodeId, orgId: $orgId, nodeCode: $nodeCode, userIds: $userIds, isLeader: $isLeader) {
    id
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
        country
        updatedAt
        customData
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
    'addPolicyAssignments': """
mutation addPolicyAssignments($policies: [String!]!, $targetType: PolicyAssignmentTargetType!, $targetIdentifiers: [String!]) {
  addPolicyAssignments(policies: $policies, targetType: $targetType, targetIdentifiers: $targetIdentifiers) {
    message
    code
  }
}

""",
    'addUdf': """
mutation addUdf($targetType: UDFTargetType!, $key: String!, $dataType: UDFDataType!, $label: String!, $options: String) {
  addUdf(targetType: $targetType, key: $key, dataType: $dataType, label: $label, options: $options) {
    targetType
    dataType
    key
    label
    options
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
mutation allow($resource: String!, $action: String!, $userId: String, $userIds: [String!], $roleCode: String, $roleCodes: [String!]) {
  allow(resource: $resource, action: $action, userId: $userId, userIds: $userIds, roleCode: $roleCode, roleCodes: $roleCodes) {
    message
    code
  }
}

""",
    'assignRole': """
mutation assignRole($roleCode: String, $roleCodes: [String], $userIds: [String!], $groupCodes: [String!], $nodeCodes: [String!]) {
  assignRole(roleCode: $roleCode, roleCodes: $roleCodes, userIds: $userIds, groupCodes: $groupCodes, nodeCodes: $nodeCodes) {
    message
    code
  }
}

""",
    'bindPhone': """
mutation bindPhone($phone: String!, $phoneCode: String!) {
  bindPhone(phone: $phone, phoneCode: $phoneCode) {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
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
    'createOrg': """
mutation createOrg($name: String!, $code: String, $description: String) {
  createOrg(name: $name, code: $code, description: $description) {
    id
    rootNode {
      id
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
mutation createPolicy($code: String!, $description: String, $statements: [PolicyStatementInput!]!) {
  createPolicy(code: $code, description: $description, statements: $statements) {
    code
    assignmentsCount
    isDefault
    description
    statements {
      resource
      actions
      effect
    }
    createdAt
    updatedAt
  }
}

""",
    'createRole': """
mutation createRole($code: String!, $description: String, $parent: String) {
  createRole(code: $code, description: $description, parent: $parent) {
    code
    arn
    description
    isSystem
    createdAt
    updatedAt
    users {
      totalCount
    }
    parent {
      code
      description
      isSystem
      createdAt
      updatedAt
    }
  }
}

""",
    'createSocialConnection': """
mutation createSocialConnection($input: CreateSocialConnectionInput!) {
  createSocialConnection(input: $input) {
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
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
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
mutation deletePolicies($codes: [String!]!) {
  deletePolicies(codes: $codes) {
    message
    code
  }
}

""",
    'deletePolicy': """
mutation deletePolicy($code: String!) {
  deletePolicy(code: $code) {
    message
    code
  }
}

""",
    'deleteRole': """
mutation deleteRole($code: String!) {
  deleteRole(code: $code) {
    message
    code
  }
}

""",
    'deleteRoles': """
mutation deleteRoles($codes: [String!]!) {
  deleteRoles(codes: $codes) {
    succeedCount
    failedCount
    message
    errors
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
    userPoolId
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
  }
}

""",
    'loginByPhoneCode': """
mutation loginByPhoneCode($input: LoginByPhoneCodeInput!) {
  loginByPhoneCode(input: $input) {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
  }
}

""",
    'loginByPhonePassword': """
mutation loginByPhonePassword($input: LoginByPhonePasswordInput!) {
  loginByPhonePassword(input: $input) {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
  }
}

""",
    'loginByUsername': """
mutation loginByUsername($input: LoginByUsernameInput!) {
  loginByUsername(input: $input) {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
  }
}

""",
    'moveNode': """
mutation moveNode($orgId: String!, $nodeId: String!, $targetParentId: String!) {
  moveNode(orgId: $orgId, nodeId: $nodeId, targetParentId: $targetParentId) {
    id
    rootNode {
      id
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
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
  }
}

""",
    'registerByPhoneCode': """
mutation registerByPhoneCode($input: RegisterByPhoneCodeInput!) {
  registerByPhoneCode(input: $input) {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
  }
}

""",
    'registerByUsername': """
mutation registerByUsername($input: RegisterByUsernameInput!) {
  registerByUsername(input: $input) {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
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
        country
        updatedAt
        customData
      }
    }
  }
}

""",
    'removePolicyAssignments': """
mutation removePolicyAssignments($policies: [String!]!, $targetType: PolicyAssignmentTargetType!, $targetIdentifiers: [String!]) {
  removePolicyAssignments(policies: $policies, targetType: $targetType, targetIdentifiers: $targetIdentifiers) {
    message
    code
  }
}

""",
    'removeUdf': """
mutation removeUdf($targetType: UDFTargetType!, $key: String!) {
  removeUdf(targetType: $targetType, key: $key) {
    targetType
    dataType
    key
    label
    options
  }
}

""",
    'removeUdv': """
mutation removeUdv($targetType: UDFTargetType!, $targetId: String!, $key: String!) {
  removeUdv(targetType: $targetType, targetId: $targetId, key: $key) {
    key
    dataType
    value
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
mutation revokeRole($roleCode: String, $roleCodes: [String], $userIds: [String!], $groupCodes: [String!], $nodeCodes: [String!]) {
  revokeRole(roleCode: $roleCode, roleCodes: $roleCodes, userIds: $userIds, groupCodes: $groupCodes, nodeCodes: $nodeCodes) {
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
    'setUdv': """
mutation setUdv($targetType: UDFTargetType!, $targetId: String!, $key: String!, $value: String!) {
  setUdv(targetType: $targetType, targetId: $targetId, key: $key, value: $value) {
    key
    dataType
    value
  }
}

""",
    'unbindPhone': """
mutation unbindPhone {
  unbindPhone {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
  }
}

""",
    'updateEmail': """
mutation updateEmail($email: String!, $emailCode: String!, $oldEmail: String, $oldEmailCode: String) {
  updateEmail(email: $email, emailCode: $emailCode, oldEmail: $oldEmail, oldEmailCode: $oldEmailCode) {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
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
    'updateNode': """
mutation updateNode($page: Int, $limit: Int, $sortBy: SortByEnum, $includeChildrenNodes: Boolean, $id: String!, $name: String, $code: String, $description: String) {
  updateNode(id: $id, name: $name, code: $code, description: $description) {
    id
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
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
  }
}

""",
    'updatePhone': """
mutation updatePhone($phone: String!, $phoneCode: String!, $oldPhone: String, $oldPhoneCode: String) {
  updatePhone(phone: $phone, phoneCode: $phoneCode, oldPhone: $oldPhone, oldPhoneCode: $oldPhoneCode) {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
  }
}

""",
    'updatePolicy': """
mutation updatePolicy($code: String!, $description: String, $statements: [PolicyStatementInput!]!) {
  updatePolicy(code: $code, description: $description, statements: $statements) {
    code
    assignmentsCount
    isDefault
    description
    statements {
      resource
      actions
      effect
    }
    createdAt
    updatedAt
  }
}

""",
    'updateRole': """
mutation updateRole($code: String!, $description: String, $newCode: String) {
  updateRole(code: $code, description: $description, newCode: $newCode) {
    code
    description
    isSystem
    createdAt
    updatedAt
    users {
      totalCount
    }
    parent {
      code
      description
      isSystem
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
    username
    email
    emailVerified
    phone
    phoneVerified
    unionid
    openid
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
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
    'addUserToGroup': """
query addUserToGroup($userId: String, $groupId: String) {
  addUserToGroup(userId: $userId, groupId: $groupId) {
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
    'getUserRoles': """
query getUserRoles($id: String!) {
  user(id: $id) {
    roles {
      totalCount
      list {
        code
        arn
        description
        isSystem
        createdAt
        updatedAt
        parent {
          code
          description
          isSystem
          createdAt
          updatedAt
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
query isActionAllowed($resource: String!, $action: String!, $userId: String!) {
  isActionAllowed(resource: $resource, action: $action, userId: $userId)
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
    'nodeByCode': """
query nodeByCode($orgId: String!, $code: String!) {
  nodeByCode(orgId: $orgId, code: $code) {
    id
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
        country
        updatedAt
        customData
      }
    }
  }
}

""",
    'nodeById': """
query nodeById($id: String!) {
  nodeById(id: $id) {
    id
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
        country
        updatedAt
        customData
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
query policies($page: Int, $limit: Int) {
  policies(page: $page, limit: $limit) {
    totalCount
    list {
      code
      assignmentsCount
      isDefault
      description
      createdAt
      updatedAt
      statements {
        resource
        actions
        effect
      }
    }
  }
}

""",
    'policy': """
query policy($code: String!) {
  policy(code: $code) {
    code
    assignmentsCount
    isDefault
    description
    statements {
      resource
      actions
      effect
    }
    createdAt
    updatedAt
  }
}

""",
    'policyAssignments': """
query policyAssignments($code: String, $targetType: PolicyAssignmentTargetType, $targetIdentifier: String, $page: Int, $limit: Int) {
  policyAssignments(code: $code, targetType: $targetType, targetIdentifier: $targetIdentifier, page: $page, limit: $limit) {
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
query role($code: String!) {
  role(code: $code) {
    code
    arn
    description
    isSystem
    createdAt
    updatedAt
    users {
      totalCount
    }
    parent {
      code
      arn
      description
      isSystem
      createdAt
      updatedAt
    }
  }
}

""",
    'roleWithUsers': """
query roleWithUsers($code: String!) {
  role(code: $code) {
    code
    arn
    description
    isSystem
    createdAt
    updatedAt
    parent {
      code
      description
      isSystem
      createdAt
      updatedAt
    }
    users {
      totalCount
      list {
        id
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
        country
        updatedAt
        customData
      }
    }
  }
}

""",
    'roles': """
query roles($page: Int, $limit: Int, $sortBy: SortByEnum) {
  roles(page: $page, limit: $limit, sortBy: $sortBy) {
    totalCount
    list {
      code
      arn
      description
      isSystem
      createdAt
      updatedAt
      parent {
        code
        description
        isSystem
        createdAt
        updatedAt
      }
    }
  }
}

""",
    'searchUser': """
query searchUser($query: String!, $fields: [String], $page: Int, $limit: Int) {
  searchUser(query: $query, fields: $fields, page: $page, limit: $limit) {
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
      country
      createdAt
      updatedAt
      customData
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
    'udv': """
query udv($targetType: UDFTargetType!, $targetId: String!) {
  udv(targetType: $targetType, targetId: $targetId) {
    key
    dataType
    value
  }
}

""",
    'user': """
query user($id: String) {
  user(id: $id) {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
  }
}

""",
    'userBatch': """
query userBatch($ids: [String!]!) {
  userBatch(ids: $ids) {
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
    identities {
      openid
      userIdInIdp
      userId
      connectionId
      isSocial
      provider
      userPoolId
    }
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
    country
    createdAt
    updatedAt
    customData
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
      description
      secret
      jwtSecret
      logo
      createdAt
      updatedAt
      emailVerifiedDefault
      sendWelcomeEmail
      registerDisabled
      showWxQRCodeWhenRegisterDisabled
      allowedOrigins
      tokenExpiresAfter
      isDeleted
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
      country
      createdAt
      updatedAt
      customData
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
