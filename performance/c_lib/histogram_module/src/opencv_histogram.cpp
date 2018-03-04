#include "opencv_histogram.hpp"

cv::Mat calculateOpenCVHistogram(const char *photoFile) {
	cv::Mat photo = cv::imread(photoFile);
        cv::Mat histogram;
        int channels[] = { 0 };
        int histSize[] = { 256 };
        float range[] = { 0, 256 };
        const float* ranges[] = { range };

        cv::Mat channel[3];
        cv::split(photo, channel);

        cv::Mat acc(photo.size(), CV_64F, cv::Scalar(0));
        accumulate(channel[0], acc);
        accumulate(channel[1], acc);
        accumulate(channel[2], acc);
        cv::Mat avg;

        acc.convertTo(avg, CV_8U, 1.0/3);

        cv::calcHist(&avg, 1, channels, cv::Mat(), histogram, 1, histSize, ranges, true, false);

        histogram = histogram.t();

	return histogram;
}

