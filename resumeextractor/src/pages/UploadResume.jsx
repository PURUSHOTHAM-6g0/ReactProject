import React, { useState } from "react";
import { Button, Container, Typography, Box, CircularProgress } from "@mui/material";
import axios from "../api/axios";

export default function UploadResume() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await axios.post("/resume/upload", formData);
      setResult(res.data);
    } catch (err) {
      alert("Upload failed");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!result) return;

    try {
      const res = await axios.post("/resume/download_resume", result, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = "generated_resume.pdf";
      a.click();
    } catch (err) {
      alert("Download failed");
      console.error(err);
    }
  };

  const handlePreviewToggle = () => {
    setShowPreview(!showPreview);
  };

  return (
    <Container>
      <Box mt={5} display="flex" flexDirection="column" alignItems="center">
        <Typography variant="h4" gutterBottom>
          Upload Resume
        </Typography>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          accept=".pdf,.doc,.docx"
        />
        <Button variant="contained" color="secondary" onClick={handleUpload} sx={{ mt: 2 }}>
          Upload
        </Button>
        {loading && <CircularProgress sx={{ mt: 2 }} />}

        {result && (
          <Box mt={4} width="100%">
            <Button
              variant="contained"
              color="secondary"
              onClick={handlePreviewToggle}
              sx={{ mb: 3 }}
            >
              {showPreview ? "Hide Preview" : "Preview"}
            </Button>

            {showPreview && (
              <Box>
                <Typography variant="h5" gutterBottom>
                  Resume Preview:
                </Typography>

                <Box mb={3}>
                  <Typography variant="h6" color="secondary">
                    <strong>Name:</strong> {result.name || "Not Available"}
                  </Typography>
                  <Typography variant="h6" color="secondary">
                    <strong>Email:</strong> {result.email || "Not Available"}
                  </Typography>
                  <Typography variant="h6" color="secondary">
                    <strong>Phone:</strong> {result.phone || "Not Available"}
                  </Typography>
                </Box>

                {/* Education */}
                <Box mb={3}>
                  <Typography variant="h6" color="secondary">
                    <strong>Education:</strong>
                  </Typography>
                  {Array.isArray(result.education) && result.education.length > 0 ? (
                    result.education.map((edu, index) => (
                      <Box key={index} mb={2}>
                        <Typography>
                          <strong>Degree:</strong> {edu.degree || "Not Available"}
                        </Typography>
                        <Typography>
                          <strong>Institution:</strong> {edu.institution || "Not Available"}
                        </Typography>
                        <Typography>
                          <strong>Location:</strong> {edu.location || "Not Available"}
                        </Typography>
                        <Typography>
                          <strong>CGPA:</strong> {edu.cgpa || "Not Available"}
                        </Typography>
                      </Box>
                    ))
                  ) : (
                    <Typography>Not Available</Typography>
                  )}
                </Box>

                {/* Skills */}
                <Box mb={3}>
                  <Typography variant="h6" color="secondary">
                    <strong>Skills:</strong>
                  </Typography>
                  {Array.isArray(result.skills) && result.skills.length > 0 ? (
                    <Box mt={1}>
                      {result.skills.map((skill, index) => (
                        <Typography key={index}>{skill}</Typography>
                      ))}
                    </Box>
                  ) : (
                    <Typography>Not Available</Typography>
                  )}
                </Box>

                {/* Experience */}
                <Box mb={3}>
                  <Typography variant="h6" color="secondary">
                    <strong>Experience:</strong>
                  </Typography>
                  {Array.isArray(result.experience) && result.experience.length > 0 ? (
                    result.experience.map((exp, index) => (
                      <Box key={index} mb={2}>
                        <Typography>
                          <strong>Role:</strong> {exp.role || "Not Available"}
                        </Typography>
                        <Typography>
                          <strong>Company:</strong> {exp.company || "Not Available"}
                        </Typography>
                        <Typography>
                          <strong>Description:</strong> {exp.description || "Not Available"}
                        </Typography>
                      </Box>
                    ))
                  ) : (
                    <Typography>Not Available</Typography>
                  )}
                </Box>

                {/* Projects */}
                <Box mb={3}>
                  <Typography variant="h6" color="secondary">
                    <strong>Projects:</strong>
                  </Typography>
                  {Array.isArray(result.projects) && result.projects.length > 0 ? (
                    result.projects.map((project, index) => (
                      <Box key={index} mb={2}>
                        <Typography>
                          <strong>Project Name:</strong> {project.name || "Not Available"}
                        </Typography>
                        <Typography>
                          <strong>Description:</strong> {project.description || "Not Available"}
                        </Typography>
                      </Box>
                    ))
                  ) : (
                    <Typography>Not Available</Typography>
                  )}
                </Box>

                {/* Certifications */}
                <Box mb={3}>
                  <Typography variant="h6" color="secondary">
                    <strong>Certifications:</strong>
                  </Typography>
                  {Array.isArray(result.certifications) && result.certifications.length > 0 ? (
                    result.certifications.map((cert, index) => (
                      <Typography key={index}>{cert}</Typography>
                    ))
                  ) : (
                    <Typography>Not Available</Typography>
                  )}
                </Box>

                {/* Interests/Hobbies */}
                <Box mb={3}>
                  <Typography variant="h6" color="secondary">
                    <strong>Interests/Hobbies:</strong>
                  </Typography>
                  <Typography>{result["interests/hobbies"] || "Not Available"}</Typography>
                </Box>

                <Button variant="contained" color="secondary" onClick={handleDownload} sx={{ mt: 3 }}>
                  Download Resume
                </Button>
              </Box>
            )}
          </Box>
        )}
      </Box>
    </Container>
  );
}
