import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProgressBar = ({ count, total, color }) => {
  const percentage = total > 0 ? (count / total) * 100 : 0;
  console.log('Foo', count, total);

  return (
    <div className="vote-bar">
      <div className="vote-bar-progress" style={{ width: `${percentage}%`, backgroundColor: color ?? '#00b1e2' }} />
      <div className="vote-bar-text">{`${percentage.toFixed(2)}% (${count} out of ${total})`}</div>
    </div>
  );
};

function App() {
  const [proposals, setProposals] = useState([]);
  const [storyHistory, setStoryHistory] = useState([]);
  const [timeInfo, setTimeInfo] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);  // New state variable for the image URL

  useEffect(() => {
    async function fetchData() {
      const proposalsRes = await axios.get('http://localhost:9511/proposals');
      setProposals(proposalsRes.data);

      const storyHistoryRes = await axios.get('http://localhost:9511/story-history');
      setStoryHistory(storyHistoryRes.data);

      const timeInfo = await axios.get('http://localhost:9511/vote-time-remaining')
      setTimeInfo(timeInfo.data);
    }

    fetchData();  // Fetch data immediately on component mount
    const intervalId = setInterval(fetchData, 1000);  // Fetch data every second

    // Clean up function: This will be run when the component is unmounted
    return () => clearInterval(intervalId);
  }, []);

  const badgeStyle = {
    display: "inline-block",
    padding: ".2em .6em .3em",
    fontSize: "75%",
    fontWeight: "700",
    lineHeight: "1",
    color: "#dddddd",
    textAlign: "center",
    whiteSpace: "nowrap",
    verticalAlign: "baseline",
    borderRadius: ".25em",
    backgroundColor: "#494949",
    margin: "0 5px"
  };

  const totalVotes = Math.max(1, proposals.map(x => x.vote).reduce((a, b) => a + b, 0));

  // New function to generate an image
  async function generateImage(prompt) {
    const response = await axios.post('http://localhost:8000/generate-image', { prompt });
    const imageUrl = response.data.image_url;
    setImageUrl(imageUrl);  // Update the image URL state variable
  }

  return (
    <div className="site-container">
      <div className="page-column main-column">
        <h2 style={{ marginBottom: '0px' }}>Story</h2>
        {storyHistory.map((entry, index) => (
          <div key={index} className="card">
            {entry.story_action ? <p><i>{entry.story_action}</i></p> : <></>}
            <p>{entry.narration_result}</p>
          </div>
        ))}
        {/* New: Display the generated image */}
        {imageUrl && <img src={imageUrl} alt="Generated" />}
      </div>

      <div className="page-column chat-column">
        <h2 style={{ marginBottom: '0px' }}>Proposals</h2>
        <div>
          {timeInfo ? <ProgressBar count={timeInfo.seconds_remaining} total={timeInfo.total_seconds} color='#eb9500' /> : proposals?.length ? <p>Loading...</p> : <p>No proposals.</p>}
        </div>
        {timeInfo && proposals.map((proposal, index) => (
          <div key={index} style={{ position: 'relative' }} className="card response-card">
            <div>
              <p><b>{index + 1}: </b>{proposal.message}</p>
            </div>
            <div>
              <ProgressBar count={proposal.vote} total={totalVotes} />
            </div>

            <div style={{ alignSelf: 'flex-start', position: 'absolute', top: 0, right: 0 }}>
              <p style={{ ...badgeStyle }}>{proposal.user}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
