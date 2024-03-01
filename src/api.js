const query = async (data) => {
    const response = await fetch("https://api-inference.huggingface.co/models/gpt2", {
      headers: { Authorization: "Bearer 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" },
      method: "POST",
      body: JSON.stringify({
        inputs: data.inputs,
        options: {
          wait_for_model: true,
          max_length: 1000,
          temperature: 0.7,
          top_p: 0.95,
          num_return_sequences: 1,
        },
      }),
    });
  
    const result = await response.json();
    return result;
  };
  
  export default query;
  