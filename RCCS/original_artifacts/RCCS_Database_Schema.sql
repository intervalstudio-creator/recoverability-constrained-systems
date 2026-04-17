CREATE TABLE identities (
  id TEXT PRIMARY KEY,
  identity_type TEXT NOT NULL CHECK (identity_type IN ('human','organization')),
  display_name TEXT NOT NULL,
  verification_status TEXT NOT NULL CHECK (verification_status IN ('pending','verified','rejected')),
  trust_state TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE messages (
  id TEXT PRIMARY KEY,
  author_id TEXT NOT NULL REFERENCES identities(id),
  claim TEXT NOT NULL,
  context TEXT,
  reference_url TEXT,
  state TEXT NOT NULL CHECK (state IN ('unverified','contested','under_resolution','stable','corrected','invalid')),
  propagation_level INTEGER NOT NULL DEFAULT 0,
  carrier TEXT NOT NULL DEFAULT 'offline_runtime' CHECK (carrier IN ('human','paper','offline_runtime')),
  ack_required BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE challenges (
  id TEXT PRIMARY KEY,
  message_id TEXT NOT NULL REFERENCES messages(id),
  challenger_id TEXT NOT NULL REFERENCES identities(id),
  challenge_type TEXT NOT NULL CHECK (challenge_type IN ('factual_contradiction','logical_inconsistency','missing_evidence','misleading_framing')),
  reason TEXT NOT NULL,
  state TEXT NOT NULL DEFAULT 'open',
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE resolutions (
  id TEXT PRIMARY KEY,
  message_id TEXT NOT NULL REFERENCES messages(id),
  outcome TEXT NOT NULL CHECK (outcome IN ('stable','corrected','invalid')),
  summary TEXT NOT NULL,
  resolved_at TIMESTAMP NOT NULL
);

CREATE TABLE exposures (
  id TEXT PRIMARY KEY,
  message_id TEXT NOT NULL REFERENCES messages(id),
  viewer_id TEXT NOT NULL REFERENCES identities(id),
  seen_at TIMESTAMP NOT NULL,
  correction_delivered BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE acknowledgments (
  id TEXT PRIMARY KEY,
  message_id TEXT NOT NULL REFERENCES messages(id),
  actor_id TEXT NOT NULL REFERENCES identities(id),
  ack_type TEXT NOT NULL CHECK (ack_type IN ('received','relayed','challenged','resolved')),
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE relays (
  id TEXT PRIMARY KEY,
  message_id TEXT NOT NULL REFERENCES messages(id),
  from_actor_id TEXT NOT NULL REFERENCES identities(id),
  to_actor_id TEXT NOT NULL REFERENCES identities(id),
  carrier TEXT NOT NULL CHECK (carrier IN ('human','paper','offline_runtime')),
  created_at TIMESTAMP NOT NULL
);
