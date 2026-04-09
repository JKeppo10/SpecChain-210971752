# Requirement ID: FR_hybrid_1
- Description: The system shall provide a variety of meditation and sleep sessions with different durations, including sessions of 5 minutes or less, to accommodate users across different usage contexts.
- Source Persona: The Satisfied User
- Traceability: Derived from review group G1
- Acceptance Criteria: Given the user is browsing the content library, When the user filters or sorts sessions by duration, Then the system displays sessions across multiple duration ranges including at least one option of 5 minutes or less.
- Notes: Carried over from FR_auto_1. Updated persona name to The Satisfied User (P_hybrid_1). Description tightened to remove the unsupported assumption about "limited time" users and instead ground the requirement in content variety, which is supported by G1 reviews.

# Requirement ID: FR_hybrid_2
- Description: The system shall ensure that active audio sessions are not interrupted by in-sytem notifications, in-system prompts, or any event triggered within the system itself.
- Source Persona: The Satisfied User
- Traceability: Derived from review group G1
- Acceptance Criteria: Given the user has started an audio session, When a notification arrives or the user switches away from and returns to the app, Then the audio session shall continue playing without pausing, skipping, or terminating.
- Notes: Replaced FR_auto_2 (daily meditation reminder). The reminder requirement was not supported by any G1 hybrid reviews. G1 reviews consistently describe interrupted playback as a frustration for otherwise satisfied users, making this a better-grounded requirement for P_hybrid_1.

# Requirement ID: FR_hybrid_3
- Description: The system shall allow users to cancel their subscription entirely from within the app without being redirected to an external platform or requiring contact with customer support.
- Source Persona: The Billing Victim
- Traceability: Derived from review group G2
- Acceptance Criteria: Given the user has an active subscription and wishes to cancel, When the user navigates to subscription settings and selects cancel, Then the subscription is cancelled and the user receives an in-app confirmation that no further charges will be applied.
- Notes: Replaced FR_auto_3 (free version with limited content). The original requirement did not fit G2 hybrid which is specifically about billing and cancellation complaints, not free-tier access. This requirement is directly grounded in G2 reviews describing the inability to cancel without being looped back to the app store.

# Requirement ID: FR_hybrid_4
- Description: The system shall display the full subscription price, billing frequency, and trial terms to the user before any payment information is requested.
- Source Persona: The Billing Victim
- Traceability: Derived from review group G2
- Acceptance Criteria: Given a new user is completing the sign-up or trial activation flow, When they are prompted to enter payment details, Then the subscription price, billing frequency, and trial end date shall have been displayed on a previous screen in the same flow.
- Notes: Replaced FR_auto_4 (free trial period). G2 hybrid reviews repeatedly describe being charged unexpectedly with no prior warning of pricing terms. The original requirement assumed G2 users wanted a free trial; the evidence shows they wanted transparency before being charged.

# Requirement ID: FR_hybrid_5
- Description: The system shall allow users to find content by content type, narrator name, or theme.
- Source Persona: The Content Critic
- Traceability: Derived from review group G3
- Acceptance Criteria: Given the user is on any screen within the app, When the user enters a keyword into the search bar, Then the system displays matching content results within 2 seconds.
- Notes: Carried over from FR_auto_5. Updated persona name to The Content Critic (P_hybrid_3). Description made more specific by listing example search input types supported by G3 reviews.

# Requirement ID: FR_hybrid_6
- Description: The system shall allow users to filter content.
- Source Persona: The Content Critic
- Traceability: Derived from review group G3
- Acceptance Criteria: Given the user is on the content library screen, When the user selects a content category filter, Then only content matching that category is displayed and all other content is hidden.
- Notes: Replaced FR_auto_6 (navigation menu labels). The original requirement was too generic. G3 hybrid reviews specifically describe difficulty finding content by type, making content filtering a more grounded and testable requirement.

# Requirement ID: FR_hybrid_7
- Description: The system shall detect repeated login failures and present the user with account recovery options without requiring them to contact support.
- Source Persona: The Blocked User
- Traceability: Derived from review group G4
- Acceptance Criteria: Given the user has failed to log in three or more consecutive times, When the next login attempt fails, Then the system shall display account recovery options such as password reset or email verification on the same screen.
- Notes: Rewrote FR_auto_7 which was too generic. The original acceptance criteria ("successfully logged in") described a happy path only. G4 hybrid reviews specifically describe login failures with no recovery path, making this a more grounded and testable requirement.

# Requirement ID: FR_hybrid_8
- Description: The system shall resume an audio session from the point of interruption when the app is reopened after a crash or unexpected closure.
- Source Persona: The Blocked User
- Traceability: Derived from review group G4
- Acceptance Criteria: Given the user was in an active audio session when the app crashed or was unexpectedly closed, When the user reopens the app, Then the app shall launch without error and offer the user the option to resume the session from the point at which it was interrupted.
- Notes: Replaced FR_auto_8 (troubleshooting instructions). Help documentation is not supported by G4 hybrid reviews. G4 reviews consistently describe crashes and unexpected app closures during sessions, making crash recovery a more directly grounded requirement for P_hybrid_4.

# Requirement ID: FR_hybrid_9
- Description: The system shall display a comparison of what is included in the free tier versus the paid subscription before prompting the user to subscribe.
- Source Persona: The Value Skeptic
- Traceability: Derived from review group G5
- Acceptance Criteria: Given the user encounters a paywalled content item, When they are shown the subscription prompt, Then the prompt shall include a visible breakdown of what content and features are available for free versus what requires a subscription.
- Notes: Carried over from FR_auto_9 with a more specific description. The original requirement was vague about "unique features". G5 hybrid reviews specifically describe users not understanding what they get for the price, making a free vs paid breakdown a directly grounded requirement.

# Requirement ID: FR_hybrid_10
- Description: The system shall allow users to access at least one complete sleep story, one soundscape, and one meditation session without a subscription.
- Source Persona: The Value Skeptic
- Traceability: Derived from review group G5
- Acceptance Criteria: Given the user has not subscribed, When the user selects a designated free content item from each of the three content types, Then each item shall play in full without a subscription prompt appearing.
- Notes: Replaced FR_auto_10 (personalized recommendations). Personalized recommendations are not mentioned in any G5 hybrid reviews. G5 reviews consistently describe the inability to evaluate the app before paying, making free content access a well-grounded requirement for P_hybrid_5.

# Requirement ID: NFR_hybrid_1
- Description: The system shall begin playing any audio session within 3 seconds of the user tapping the play button.
- Source Persona: The Satisfied User
- Traceability: Derived from review group G1
- Acceptance Criteria: Given the user has selected an audio session and tapped the play button, When the tap is registered by the system, Then audio playback shall begin within 3 seconds.
- Notes: Carried over from NFR_auto_1. Updated persona name. Removed the phrase "seamless user experience" which is ambiguous. Load time kept as a measurable threshold. Changed from 2 to 3 seconds to be more realistic across device types.

# Requirement ID: NFR_hybrid_2
- Description: The system shall process a subscription cancellation request and confirm it to the user within the same app session in which the request was made.
- Source Persona: The Billing Victim
- Traceability: Derived from review group G2
- Acceptance Criteria: Given the user has submitted a cancellation request, When the request is processed, Then the system shall display a cancellation confirmation screen within the same session without requiring the user to re-authenticate or restart the app.
- Notes: Rewrote NFR_auto_2 which used vague terms such as "easily", "clear", and "straightforward". The revised requirement is specific and testable, grounded in G2 evidence of users being unable to complete cancellation in a single session.

# Requirement ID: NFR_hybrid_3
- Description: The system shall not deliver notifications to the user while an audio session is actively playing.
- Source Persona: The Content Critic
- Traceability: Derived from review group G3
- Acceptance Criteria: Given the user has an active audio session playing, When any in-app notification is triggered, Then the notification shall be suppressed and not delivered until the session has ended or the user has manually paused it.
- Notes: Replaced NFR_auto_3 which used untestable language including "simple and intuitive" and "rates ease of use 4 or 5 out of 5". Notification interruptions during sessions are a specific and recurring pain point in G3 hybrid reviews, making this a better-grounded NFR for P_hybrid_3.

# Requirement ID: NFR_hybrid_4
- Description: When the app encounters an unexpected error during normal use, the system shall display a descriptive error message and present the user with at least one recovery action rather than becoming silently unresponsive or closing without notice.
- Source Persona: The Blocked User
- Traceability: Derived from review group G4
- Acceptance Criteria: Given the app encounters an unexpected error during audio playback, content browsing, or login on a supported Android device, When the error occurs, Then the app shall display a message describing the problem and offer the user at least one actionable option such as retry or return to home screen, rather than freezing silently or closing without explanation.
- Notes: Refined from previous version which unrealistically required the app to never crash. Crashes can occur due to external factors beyond the app's control. The requirement now focuses on graceful error handling — ensuring users are informed and given a path forward when errors do occur, which is directly supported by G4 reviews describing silent failures and unexplained closures.

# Requirement ID: NFR_hybrid_5
- Description: The system shall load any content item selected by the user and begin playback within 4 seconds on a standard mobile data connection.
- Source Persona: The Value Skeptic
- Traceability: Derived from review group G5
- Acceptance Criteria: Given the user has selected a content item to play while connected to a standard mobile data network, When the item is selected, Then playback shall begin within 4 seconds without requiring the user to retry.
- Notes: Replaced NFR_auto_5 which used vague language including "seamless", "intuitive", and an arbitrary "3 clicks" measure. A load time threshold is specific and testable. Grounded in G5 evidence where slow or failing content loads contribute to users questioning the app's value versus free alternatives.