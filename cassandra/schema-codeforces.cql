USE kafkapipeline;
DROP TABLE IF EXISTS kafkapipeline.codeforcesdata;
CREATE TABLE IF NOT EXISTS kafkapipeline.codeforcesdata (
    handle TEXT PRIMARY KEY,                               
    rating INT,                                                
    rank TEXT,                                          
    max_rating INT,                                             
    max_rank TEXT,                                       
    last_online_time INT,                                 
    registration_time INT,                               
    contribution INT,                                         
    country TEXT                                     
);

