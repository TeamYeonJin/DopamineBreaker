import { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import { formatTimeToMMSS, getMissionTitle, requestNotificationPermission, sendNotification } from "../utils/helpers";

const TimerContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 85vh;
  gap: 48px;
`;

const MissionTitle = styled.h2`
  font-size: 32px;
  font-weight: 700;
  color: #333333;
  text-align: center;
`;

const TimerDisplay = styled.div`
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3a6ea5 0%, #2b5e95 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  position: relative;

  &::before {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background-color: #ffffff;
  }
`;

const Time = styled.div`
  font-size: 4rem;
  font-weight: 700;
  color: #333333;
  z-index: 1;
  font-variant-numeric: tabular-nums;
`;

const MissionDescription = styled.p`
  font-size: 18px;
  color: #757575;
  text-align: center;
  max-width: 500px;
  line-height: 1.6;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 24px;
`;

const Button = styled.button`
  padding: 16px 48px;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  transition: all 0.15s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
`;

const CancelButton = styled(Button)`
  background-color: #ffffff;
  color: #333333;
  border: 2px solid #e0e0e0;

  &:hover {
    border-color: #757575;
  }
`;

const CompleteButton = styled(Button)`
  background-color: #4caf50;
  color: white;

  &:hover {
    background-color: #45a049;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;

const FocusAlert = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #ffffff;
  padding: 48px;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  text-align: center;
  z-index: 1000;
  display: ${(props) => (props.show ? "block" : "none")};

  h3 {
    font-size: 24px;
    color: #3a6ea5;
    margin-bottom: 16px;
  }

  p {
    font-size: 18px;
    color: #757575;
  }
`;

const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  display: ${(props) => (props.show ? "block" : "none")};
`;

function MissionTimer({ mission, onComplete, onCancel }) {
  const [timeLeft, setTimeLeft] = useState(mission.duration * 60);
  const [isCompleted, setIsCompleted] = useState(false);
  const [showFocusAlert, setShowFocusAlert] = useState(false);
  const intervalRef = useRef(null);
  const missionTitle = getMissionTitle(mission);

  useEffect(() => {
    requestNotificationPermission();

    intervalRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(intervalRef.current);
          setIsCompleted(true);
          sendNotification("미션 완료!", `${missionTitle} 미션을 완료했습니다!`);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    const handleVisibilityChange = () => {
      if (document.hidden && !isCompleted) {
        setShowFocusAlert(true);
        setTimeout(() => setShowFocusAlert(false), 3000);
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      clearInterval(intervalRef.current);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [missionTitle, isCompleted]);

  const handleComplete = () => {
    clearInterval(intervalRef.current);
    onComplete();
  };

  const handleCancel = () => {
    clearInterval(intervalRef.current);
    onCancel();
  };

  return (
    <>
      <TimerContainer>
        <MissionTitle>{missionTitle}</MissionTitle>

        <TimerDisplay>
          <Time>{formatTimeToMMSS(timeLeft)}</Time>
        </TimerDisplay>

        <MissionDescription>{mission.description}</MissionDescription>

        <ButtonGroup>
          <CancelButton onClick={handleCancel}>취소</CancelButton>
          <CompleteButton onClick={handleComplete} disabled={!isCompleted}>
            {isCompleted ? "완료하기" : "진행 중..."}
          </CompleteButton>
        </ButtonGroup>
      </TimerContainer>

      <Overlay show={showFocusAlert} />
      <FocusAlert show={showFocusAlert}>
        <h3>집중 모드 중입니다!</h3>
        <p>앱으로 다시 돌아와주세요</p>
      </FocusAlert>
    </>
  );
}

export default MissionTimer;
