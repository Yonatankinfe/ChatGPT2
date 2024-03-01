import './index.css';
import './index.css';

function Body({ texts }) {
  return (
    <div className="card">
      {texts.map(({ user, assistant }, index) => (
        <>
          <div className="userText" key={index}>
          {user}
          </div>
          <div className="assistantText" key={index}>
            {assistant}
          </div>
        </>
      ))}
    </div>
  );
}

export default Body;