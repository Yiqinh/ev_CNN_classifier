import { useState, useRef } from "react";

function App() {
  const [imageUrl, setImageUrl] = useState(null);
  const imageRef = useRef();

  const [results, setResults] = useState([]);

  const uploadImage = async (e) => {
    const { files } = e.target;
    if (files.length > 0) {
      const url = URL.createObjectURL(files[0]);
      setImageUrl(url);

      const file = e.target.files[0];
      const data = new FormData();
      data.append("file_from_react", file);

      let response = await fetch("/cnn", {
        method: "post",
        body: data,
      });
      let res = await response.json();

      console.log(res.status);
      if (res.status !== 'OPEN SEASAME') {
        alert("Error uploading file");
      }
    } else {
      setImageUrl(null);
    }
  };

  const inference = async (e) => {
    let response = await fetch("/infer", {
      method: "post",
      body: "perform inference",
    });
    let res = await response.json();
  }

  const CnnResult = ({ is_pineapple, confidence, isTopResult }) => (
    <div className={`pineapple-result ${isTopResult ? "top-result" : ""}`}>
      <div className="pineapple-header">
        <span className="pizza-name">{is_pineapple.toUpperCase()}</span>
        {isTopResult && <span className="best-guess">Best Guess</span>}
      </div>
      <div className="confidence-level">
        Confidence level: {confidence.toFixed(2)}%
      </div>
    </div>
  );

  const PizzaTypeResults = ({ results }) => (
    <div className="inference-results">
      {results.map((result, index) => (
        <CnnResult
          key={result.pizza}
          is_pineapple={result.pizza}
          confidence={result.confidence}
          isTopResult={result.top}
        />
      ))}
    </div>
  );

  const sampleResults = [
    { pizza: "Pineapple", confidence: 24.47, top: false },
    { pizza: "No Pineapple", confidence: 38.37, top: true },
  ];

  return (
    <div className="App">
      <h1 className="header">Pineapple Pizza Classification</h1>
      <div className="inputHolder">
        <input
          type="file"
          accept="image/jpg, image/jpeg, image/png"
          className="uploadInput"
          onChange={uploadImage}
        />
      </div>
      <div className="mainWrapper">
        <div className="mainContent">
          <div className="imageHolder">
            {imageUrl && (
              <img
                src={imageUrl}
                alt="Upload Preview"
                crossOrigin="anonymous"
                ref={imageRef}
              />
            )}
          </div>
          <PizzaTypeResults results={sampleResults} />
        </div>
        {imageUrl && <button className="button">Identify Image</button>}
      </div>
    </div>
  );
}

export default App;
