# Calm App — Manual Requirements Specification

## Functional Requirements

# Requirement ID: FR1
- Description: The system shall ensure that active audio sessions are not interrupted by notifications, incoming prompts, or the user switching away from and returning to the app.
- Source Persona: Successful Sleepers/Stress Relievers
- Traceability: Derived from review group G1
- Acceptance Criteria: Given the user has started an audio session, When a notification arrives or the user switches away from and returns to the app, Then the audio session shall continue playing without pausing, skipping, or terminating.

# Requirement ID: FR2
- Description: The system shall allow users to define a time window during which the app shall not send any notifications or prompts.
- Source Persona: Successful Sleepers/Stress Relievers
- Traceability: Derived from review group G1
- Acceptance Criteria: Given the user has defined a quiet hours time window, When a notification or prompt is triggered during that window, Then the notification or prompt shall not be delivered to the user until the window has ended.

# Requirement ID: FR3
- Description: The system shall allow users to set a timer so that audio playback stops automatically after a specified period.
- Source Persona: Successful Sleepers/Stress Relievers
- Traceability: Derived from review group G1
- Acceptance Criteria: Given the user has set a sleep timer before or during a session, When the specified time elapses, Then audio playback shall stop and shall not resume automatically.

# Requirement ID: FR4
- Description: The system shall allow users to find content by keyword, sound type, or category.
- Source Persona: Critic
- Traceability: Derived from review group G2
- Acceptance Criteria: Given the user queries for content using a keyword such as "thunderstorm" or "ocean", When the query is submitted, Then matching content shall be displayed to the user.

# Requirement ID: FR5
- Description: The system shall prioritise content the user has not previously played when presenting content to the user.
- Source Persona: Critic
- Traceability: Derived from review group G2
- Acceptance Criteria: Given the user has a mix of played and unplayed content available, When the system presents content to the user, Then unplayed content shall appear before previously played content.

# Requirement ID: FR6
- Description: The system shall allow users to rate individual content items, and shall factor those ratings into the order in which content is presented to that user.
- Source Persona: Critic
- Traceability: Derived from review group G2
- Acceptance Criteria: Given the user has rated one content item higher than another, When the system presents content to the user, Then the higher-rated item shall be presented before the lower-rated item, all else being equal.

# Requirement ID: FR7
- Description: The system shall allow users to exclude specific content items so that excluded content is never recommended or automatically selected for them.
- Source Persona: Critic
- Traceability: Derived from review group G2
- Acceptance Criteria: Given the user has excluded a specific content item, When the system presents or auto-selects content for that user, Then the excluded item shall not appear in recommendations or be automatically selected.

# Requirement ID: FR8
- Description: The system shall present the subscription price, billing frequency, and included features to the user before requiring account creation or payment.
- Source Persona: Value-Conscious Trialist
- Traceability: Derived from review group G3
- Acceptance Criteria: Given a new user opens the app for the first time, When they are prompted to create an account or enter payment details, Then the subscription price, billing frequency, and included features shall have already been visible to the user prior to that prompt.

# Requirement ID: FR9
- Description: The system shall allow unsubscribed users to fully access at least one meditation session, one sleep story, and one soundscape without a subscription.
- Source Persona: Value-Conscious Trialist
- Traceability: Derived from review group G3
- Acceptance Criteria: Given the user has not subscribed, When the user selects a designated free content item, Then the content shall play in full without a subscription prompt appearing.

# Requirement ID: FR10
- Description: The system shall make at least one acute anxiety relief session fully available to all users regardless of subscription status.
- Source Persona: Value-Conscious Trialist
- Traceability: Derived from review group G3
- Acceptance Criteria: Given the user has not subscribed, When the user selects an acute anxiety relief session, Then the session shall play in full without a subscription prompt appearing.

# Requirement ID: FR11
- Description: The system shall allow users to cancel their subscription without requiring contact with external support.
- Source Persona: Billing Problem User
- Traceability: Derived from review group G4
- Acceptance Criteria: Given the user wishes to cancel their subscription, When the user initiates the cancellation process, Then the subscription shall be fully cancelled and the user shall receive confirmation that no further charges will be applied, without needing to contact customer support.

# Requirement ID: FR12
- Description: The system shall notify the user at least three times before a free trial converts to a paid subscription, at one week, 48 hours, and 4 hours before the conversion occurs.
- Source Persona: Billing Problem User
- Traceability: Derived from review group G4
- Acceptance Criteria: Given the user is on a free trial, When the trial is one week, 48 hours, and 4 hours away from converting to a paid subscription, Then the user shall receive a notification at each of those intervals informing them of the upcoming charge before it occurs.

# Requirement ID: FR13
- Description: The system shall make the user's active subscription tier, next billing date, and next billing amount accessible to the user at all times.
- Source Persona: Billing Problem User
- Traceability: Derived from review group G4
- Acceptance Criteria: Given the user wishes to view their billing information, When the user navigates to their billing details, Then the current subscription tier, next billing date, and next charge amount shall all be displayed.

---

## Non-Functional Requirements

# Requirement ID: NFR1
- Description: The system shall acknowledge a user's refund request within 48 hours of submission.
- Source Persona: Billing Problem User
- Traceability: Derived from review group G4
- Acceptance Criteria: Given the user has submitted a refund request, When 48 hours have elapsed since submission, Then the user shall have received an acknowledgement containing a reference number and an expected resolution timeframe.

# Requirement ID: NFR2
- Description: The system shall recover gracefully from a crash or unexpected closure during an audio session and offer the user the option to resume from the point of interruption.
- Source Persona: App Issues User
- Traceability: Derived from review group G5
- Acceptance Criteria: Given the user was in an active audio session when the app crashed or was unexpectedly closed, When the user reopens the app, Then the app shall launch without error and offer the user the option to resume the session from the point at which it was interrupted.

# Requirement ID: NFR3
- Description: The system shall provide a consistent and predictable navigation path to all major content categories.
- Source Persona: App Issues User
- Traceability: Derived from review group G5
- Acceptance Criteria: Given the user is at the app's starting point after launch, When the user navigates to a major content category on multiple separate occasions, Then the same navigation path shall lead to the same destination each time without requiring navigation through unrelated screens.