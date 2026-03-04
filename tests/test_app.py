def test_root_redirect(client):
    """Test that root endpoint redirects to static index.html"""
    # Arrange - No special setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test that GET /activities returns all activities"""
    # Arrange - No special setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200

    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_get_activities_structure(client):
    """Test that activities have correct structure"""
    # Arrange - No special setup needed

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_for_activity(client):
    """Test signing up a participant for an activity"""
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity in result["message"]

    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity]["participants"]


def test_delete_participant(client):
    """Test removing a participant from an activity"""
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"

    # First signup the participant
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result

    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity]["participants"]


def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity returns 404"""
    # Arrange
    email = "testuser@mergington.edu"
    nonexistent_activity = "Nonexistent Activity"

    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]


def test_delete_nonexistent_participant(client):
    """Test deleting a non-existent participant returns 404"""
    # Arrange
    email = "nonexistent@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Participant not found" in result["detail"]