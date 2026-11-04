import React from 'react';
import {
	AbsoluteFill,
	Img,
	interpolate,
	spring,
	staticFile,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';

export const FONT_ARABIC_SANS = "'Cairo', 'Tajawal', 'Segoe UI', Tahoma, Arial, sans-serif";
export const FONT_SERIF = "'Amiri', Georgia, 'Times New Roman', serif";

export const FORMATS = {
	shorts: {width: 1080, height: 1920, safeTop: 220, safeBottom: 360, safeSide: 70},
	youtube: {width: 1920, height: 1080, safeTop: 120, safeBottom: 120, safeSide: 120},
	square: {width: 1080, height: 1080, safeTop: 110, safeBottom: 110, safeSide: 80},
	portrait: {width: 1080, height: 1350, safeTop: 140, safeBottom: 140, safeSide: 75},
} as const;

export const useEnter = (startSec: number, durationSec = 0.45) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const startFrame = startSec * fps;
	const progress = spring({
		frame: frame - startFrame,
		fps,
		config: {damping: 14, stiffness: 140, mass: 0.8},
	});
	const opacity = interpolate(
		frame,
		[startFrame, startFrame + durationSec * fps * 0.6],
		[0, 1],
		{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
	);
	const blur = interpolate(
		frame,
		[startFrame, startFrame + durationSec * fps * 0.8],
		[14, 0],
		{extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
	);
	return {progress, opacity, blur};
};

export const Sphere3D: React.FC<{
	size: number;
	color1: string;
	color2: string;
	style?: React.CSSProperties;
}> = ({size, color1, color2, style}) => (
	<div
		style={{
			width: size,
			height: size,
			borderRadius: '50%',
			background: `radial-gradient(circle at 32% 28%, #ffffff 0%, ${color1} 28%, ${color2} 78%, #0f172a 100%)`,
			boxShadow: `0 ${size * 0.22}px ${size * 0.45}px rgba(15, 23, 42, 0.26), inset -${size * 0.08}px -${size * 0.08}px ${size * 0.18}px rgba(0,0,0,0.35)`,
			...style,
		}}
	/>
);

export const SparkleStar: React.FC<{
	size: number;
	color?: string;
	style?: React.CSSProperties;
}> = ({size, color = '#7c3aed', style}) => (
	<svg
		width={size}
		height={size}
		viewBox="0 0 100 100"
		style={{
			filter: 'drop-shadow(0 12px 20px rgba(88, 28, 135, 0.25))',
			...style,
		}}
	>
		<defs>
			<linearGradient id={`grad-${color}`} x1="0%" y1="0%" x2="100%" y2="100%">
				<stop offset="0%" stopColor="#c084fc" />
				<stop offset="50%" stopColor={color} />
				<stop offset="100%" stopColor="#3b0764" />
			</linearGradient>
		</defs>
		<path
			d="M50 0 C54 36 64 46 100 50 C64 54 54 64 50 100 C46 64 36 54 0 50 C36 46 46 36 50 0 Z"
			fill={`url(#grad-${color})`}
		/>
	</svg>
);

export const SelectionBox: React.FC<{
	children: React.ReactNode;
	borderColor?: string;
	bg?: string;
	padding?: string;
	style?: React.CSSProperties;
}> = ({
	children,
	borderColor = '#1e1b4b',
	bg = 'rgba(255, 255, 255, 0.88)',
	padding = '18px 42px',
	style,
}) => {
	const handleSize = 14;
	const corners: React.CSSProperties[] = [
		{top: -handleSize / 2, left: -handleSize / 2},
		{top: -handleSize / 2, right: -handleSize / 2},
		{bottom: -handleSize / 2, left: -handleSize / 2},
		{bottom: -handleSize / 2, right: -handleSize / 2},
	];
	return (
		<div
			style={{
				position: 'relative',
				display: 'inline-flex',
				alignItems: 'center',
				justifyContent: 'center',
				border: `3px dashed ${borderColor}`,
				background: bg,
				padding,
				boxShadow: '0 14px 34px rgba(15, 23, 42, 0.08)',
				...style,
			}}
		>
			{corners.map((c, idx) => (
				<div
					key={idx}
					style={{
						position: 'absolute',
						width: handleSize,
						height: handleSize,
						borderRadius: '50%',
						background: borderColor,
						border: '2px solid #ffffff',
						...c,
					}}
				/>
			))}
			{children}
		</div>
	);
};

export const GridBackground: React.FC<{
	bgColor?: string;
	gridSize?: number;
}> = ({bgColor = '#ecebe6', gridSize = 54}) => {
	const frame = useCurrentFrame();
	const {durationInFrames} = useVideoConfig();
	const progressWidth = interpolate(frame, [0, durationInFrames], [0, 100]);

	return (
		<AbsoluteFill style={{backgroundColor: bgColor, overflow: 'hidden'}}>
			<AbsoluteFill
				style={{
					backgroundImage: `
						linear-gradient(to right, rgba(15, 23, 42, 0.065) 1.5px, transparent 1.5px),
						linear-gradient(to bottom, rgba(15, 23, 42, 0.065) 1.5px, transparent 1.5px)
					`,
					backgroundSize: `${gridSize}px ${gridSize}px`,
				}}
			/>
			<div
				style={{
					position: 'absolute',
					top: 0,
					left: 0,
					height: 10,
					width: `${progressWidth}%`,
					background: 'linear-gradient(90deg, #1d4ed8, #7c3aed, #f59e0b)',
				}}
			/>
		</AbsoluteFill>
	);
};

// Scene Card component for Storyboard / Generated Scene Images
export const AnimatedSceneCard: React.FC<{
	imagePath: string;
	durationInFrames: number;
	children?: React.ReactNode;
}> = ({imagePath, durationInFrames, children}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const enterSpring = spring({
		frame,
		fps,
		config: {damping: 14, stiffness: 140, mass: 0.8},
	});

	const enterOpacity = interpolate(frame, [0, 8], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	const enterBlur = interpolate(frame, [0, 10], [14, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	const pushIn = interpolate(frame, [0, durationInFrames], [1.0, 1.05], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	const floatY = Math.sin(frame / 14) * 6;

	return (
		<AbsoluteFill
			style={{
				alignItems: 'center',
				justifyContent: 'center',
				paddingTop: 110,
				paddingBottom: 110,
			}}
		>
			<div
				style={{
					width: 900,
					height: 1350,
					borderRadius: 48,
					overflow: 'hidden',
					position: 'relative',
					boxShadow: '0 32px 85px rgba(15, 23, 42, 0.18), 0 0 0 3px #ffffff',
					transform: `scale(${0.92 + 0.08 * enterSpring}) translateY(${floatY}px)`,
					opacity: enterOpacity,
					filter: `blur(${enterBlur}px)`,
				}}
			>
				<Img
					src={staticFile(imagePath)}
					style={{
						width: '100%',
						height: '100%',
						objectFit: 'cover',
						transform: `scale(${pushIn})`,
					}}
				/>
				{children}
			</div>
		</AbsoluteFill>
	);
};
