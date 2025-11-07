import { useState, useEffect } from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import DongMedal from "../assets/DongMedal.png";
import EunMedal from "../assets/EunMedal.png";
import GeumMedal from "../assets/GeumMedal.png";

const HomeContainer = styled.div`
  max-width: 480px;
  margin: 0 auto;
  padding: 24px;
  padding-bottom: 100px;
`;

const Header = styled.div`
  margin-top: 32px;
`;

const Greeting = styled.h1`
  font-size: 24px;
  font-weight: 700;
  color: #000000;
  margin-bottom: 28px;
  line-height: 1.4;
`;

const SectionTitle = styled.p`
  font-size: 22px;
  font-weight: 600;
  color: #000000;
  margin-bottom: 16px;
`;

const Section = styled.section`
  margin-bottom: 48px;
`;

const UsageCard = styled.div`
  background-color: #ffffff;
  border-radius: 16px;
  padding: 18px;
`;

const ChartContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0px;
`;

const ChartArea = styled.div`
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 260px;
  gap: 12px;
  padding: 0 16px 3px 16px;
  position: relative;
  background-image: repeating-linear-gradient(
    to top,
    transparent,
    transparent 49px,
    #d6d6d6 49px,
    #d6d6d6 50px
  );
`;

const BarWrapper = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  position: relative;
  z-index: 1;
`;

const Bar = styled.div`
  width: 100%;
  max-width: 120px;
  background: ${(props) => props.color};
  border-radius: 8px 8px 0 0;
  height: ${(props) => props.height}px;
  transition: height 0.3s ease;
`;

const BarTime = styled.div`
  font-size: 14px;
  font-weight: 400;
  margin: 0px;
  color: #000000;
`;

const BarLabel = styled.div`
  font-size: 14px;
  margin-top: 8px;
  font-weight: 400;
  color: ${(props) => props.color};
  text-align: center;
  word-break: keep-all;
`;

const MissionGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
`;

const MissionCardSmall = styled.div`
  background-color: #ffffff;
  padding: 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.15s ease;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  }
`;

const MedalIcon = styled.img`
  width: 36px;
  height: 36px;
  object-fit: contain;
`;

const MissionInfo = styled.div`
  flex: 1;
`;

const MissionTitle = styled.div`
  font-size: 15px;
  font-weight: 600;
  color: #333333;
  margin-bottom: 4px;
`;

const MissionDuration = styled.div`
  font-size: 13px;
  color: #757575;
`;

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:5001/api";

const tierConfig = {
  bronze: { label: "브론즈", medal: DongMedal },
  silver: { label: "실버", medal: EunMedal },
  gold: { label: "골드", medal: GeumMedal },
};

function Home() {
  const navigate = useNavigate();
  const [userName] = useState("사용자");
  const [currentDate, setCurrentDate] = useState("");
  const [usageData, setUsageData] = useState({
    categories: [],
  });
  const [quickMissions, setQuickMissions] = useState([]);

  useEffect(() => {
    // 현재 날짜 설정
    const date = new Date();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    setCurrentDate(`${month}월 ${day}일`);

    // TODO: API에서 사용 기록 가져오기
    // 임시 데이터
    setUsageData({
      categories: [
        { name: "엔터테인먼트", time: 150, color: "#0B84FF" },
        { name: "생산성 및 금융", time: 85, color: "#6AC4DC" },
        { name: "소셜 미디어", time: 107, color: "#FF9F0B" },
      ],
    });

    // 미션 데이터 가져오기
    const fetchMissions = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/missions/presets`);
        if (response.ok) {
          const data = await response.json();
          const missions = Array.isArray(data) ? data : data.missions;
          // 최대 4개만 가져오기
          setQuickMissions(missions.slice(0, 4));
        }
      } catch (error) {
        console.error("미션을 불러오지 못했습니다:", error);
      }
    };

    fetchMissions();
  }, []);

  const handleMissionClick = (mission) => {
    navigate("/mission", { state: { autoStartMission: mission } });
  };

  const formatTime = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}시간 ${mins}분` : `${mins}분`;
  };

  return (
    <HomeContainer>
      <Header>
        <Greeting>
          {userName}님<br />
          잠시 쉬어가볼까요?
        </Greeting>
        <SectionTitle>{currentDate} 사용 내용</SectionTitle>
      </Header>

      <Section>
        <UsageCard>
          <ChartContainer>
            <ChartArea>
              {usageData.categories.map((category, index) => {
                const maxTime = Math.max(
                  ...usageData.categories.map((c) => c.time)
                );
                const maxHeight = 200;
                const barHeight = (category.time / maxTime) * maxHeight;

                return (
                  <BarWrapper key={index}>
                    <Bar color={category.color} height={barHeight} />
                    <BarLabel color={category.color}>{category.name}</BarLabel>
                    <BarTime>{formatTime(category.time)}</BarTime>
                  </BarWrapper>
                );
              })}
            </ChartArea>
          </ChartContainer>
        </UsageCard>
      </Section>

      <Section>
        <SectionTitle>오늘의 미션</SectionTitle>
        <MissionGrid>
          {quickMissions.map((mission) => {
            const tierMeta = tierConfig[mission.tier];
            return (
              <MissionCardSmall
                key={mission.id}
                onClick={() => handleMissionClick(mission)}
              >
                {tierMeta?.medal && (
                  <MedalIcon src={tierMeta.medal} alt={`${tierMeta.label} 메달`} />
                )}
                <MissionInfo>
                  <MissionTitle>{mission.title || mission.description}</MissionTitle>
                  <MissionDuration>{mission.duration}분</MissionDuration>
                </MissionInfo>
              </MissionCardSmall>
            );
          })}
        </MissionGrid>
      </Section>
    </HomeContainer>
  );
}

export default Home;
